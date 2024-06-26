# This Python file uses the following encoding: utf-8
import os
import sys
import json

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QPlainTextEdit,
                               QMessageBox, QRadioButton, QCheckBox)
from PySide6.QtCore import Qt, QPointF

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from utils.qt import *
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate, DSDelete, ImageDeleteDialog, AddLabelDialog, DeleteLabelDialog
from ui.widget import ImageTabInnerWidget
from core.database import DBManager
from core.weedfs import SeaWeedFS
from core.qt.item import BoxQListWidgetItem
from core.qt.shape import Shape


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, cfg=None, logger=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.cfg = cfg
        self.logger = logger

        self.db_manager = DBManager(user=cfg.user,
                                    password=cfg.password,
                                    host=cfg.host,
                                    port=cfg.port,
                                    database=cfg.database,
                                    logger=logger)
        self.weed_manager = SeaWeedFS(cfg=cfg, logger=self.logger)

        # Set params
        self.cur_dataset_idx = -1
        self.cur_tab_idx = -1
        self.cur_tab_name = None
        self.cur_inner_tab = None
        self.cur_label_fields = []
        self.cur_label_fields_class = {}
        self.cur_label_fields_idx_dict = {}
        self.cur_image_idx = -1
        self.is_label_change = False

        # label fields
        self.lb_image_caps = []
        self.lb_image_cls = []
        self.lb_boxes_box = []
        self.lb_items_to_shapes = {}
        self.lb_shapes_to_items = {}

        # Inner param
        self._beginner = True
        self._no_selection_slot = False
        self._is_change_box_class = False
        self._change_box_class = []

        # init drawing
        self.draw_dataset()
        self.draw_image_list_widget()
        self.clean_label_field()
        self.draw_label_field()

        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)
        self.tB_header_uploadImage.clicked.connect(self.upload_images)
        self.actionUpload_Image.triggered.connect(self.upload_images)
        self.tB_header_uploadDir.clicked.connect(self.upload_dir)
        self.actionUpload_folder.triggered.connect(self.upload_dir)
        self.tB_header_delDataset.clicked.connect(self.delete_dataset)
        self.actionDelete_Dataset.triggered.connect(self.delete_dataset)

        self.tB_header_delSelectedImage.clicked.connect(self.delete_images)
        self.actionDelete_Selected_Image.triggered.connect(self.delete_images)
        self.actionSave_label.triggered.connect(self.save_labels)

        self.actionCreate_Mode.triggered.connect(self.set_create_mode)
        self.actionEdit_Mode.triggered.connect(self.set_edit_mode)
        self.actionSelect_up_image.triggered.connect(self.get_upper_image)
        self.actionSelect_down_image.triggered.connect(self.get_lower_image)
        self.actionDelete_selected_box.triggered.connect(self.delete_selected_boxes_box_label)

        self.tB_img_up.clicked.connect(self.get_upper_image)
        self.tB_img_down.clicked.connect(self.get_lower_image)
        self.tB_img_del.clicked.connect(self.delete_images)

        self.tW_img.currentChanged.connect(self.change_tab)

        self.tW_images.itemClicked.connect(self.draw_image)

        self.lw_labels.itemActivated.connect(self.label_selection_changed)
        self.lw_labels.itemSelectionChanged.connect(self.label_selection_changed)

        self.pB_label_add.clicked.connect(self.add_label_field)
        self.pB_label_del.clicked.connect(self.delete_label_field)

        self.logger.info("Success initializing MainWindow")

    def create_dataset(self):
        self.logger.info("Click 'dataset create'")
        ds_create = DSCreate(self, self.db_manager)
        ds_create.show()

    def upload_dir(self):
        self.logger.info("Click 'Upload dir'")
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.FileMode.Directory)
        fileDialog.setViewMode(QFileDialog.ViewMode.List)

        fileDialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        fileDialog.setOption(QFileDialog.Option.ReadOnly, True)
        fileDialog.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)
        fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

        dirname = fileDialog.getExistingDirectory(
            parent=self,
            caption='Select Directory',
            dir=""
        )

        if not dirname:
            self.logger.info("이미지 디렉토리 선택 취소")
            return
        else:
            upload_images = []
            for file in os.listdir(dirname):
                basename, ext = os.path.splitext(file)
                file_path = os.path.join(dirname, file)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                    upload_images.append(file_path)
            for f_idx, filename in enumerate(upload_images):
                self.statusbar.showMessage(f"Upload image ... ({f_idx + 1}/{len(upload_images)})")

                ret = self.weed_manager.put_image_collection(image=filename, filename=filename)

                idx = self.db_manager.create_image_data(
                    dataset_id=self.cur_dataset_idx,
                    filename=ret['filename'],
                    image_fid=ret['fid'],
                    image_url=ret['url'],
                    width=ret['width'],
                    height=ret['height']
                )
                self.tW_images.add_image_list(idx, ret['filename'], ret['fid'], ret['url'])
            self.logger.info("이미지 디렉토리 업로드 완료")
            self.statusbar.showMessage(f"Image Directory upload Success")

    def upload_images(self):
        self.logger.info("Click 'Upload image'")
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        fileDialog.setViewMode(QFileDialog.ViewMode.List)     # Detail, List
        # By default, all options are disabled.
        fileDialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        fileDialog.setOption(QFileDialog.Option.ReadOnly, True)
        fileDialog.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)
        fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

        fileNames = fileDialog.getOpenFileNames(
            parent=self,
            caption="Open Image",
            dir="",
            filter="Image Files (*.png *.jpg *.jpeg *.bmp)",
        )
        filenames, filters = fileNames
        if not filenames:
            self.logger.info("이미지 업로드 취소")
            return
        else:
            for f_idx, filename in enumerate(filenames):
                self.statusbar.showMessage(f"Upload image ... ({f_idx+1}/{len(filenames)})")

                ret = self.weed_manager.put_image_collection(image=filename, filename=filename)

                idx = self.db_manager.create_image_data(
                    dataset_id=self.cur_dataset_idx,
                    filename=ret['filename'],
                    image_fid=ret['fid'],
                    image_url=ret['url'],
                    width=ret['width'],
                    height=ret['height']
                )
                self.tW_images.add_image_list(idx, ret['filename'], ret['fid'], ret['url'])
            self.logger.info("이미지 업로드 완료")
            self.statusbar.showMessage(f"Image upload Success")

    def delete_dataset(self):
        self.logger.info("Click 'dataset delete'")
        cur_idx = self.tW_img.currentIndex()
        cur_tab_name = self.tW_img.tabText(cur_idx)

        q_delete = DSDelete(self,
                            ds_name=cur_tab_name,
                            weed=self.weed_manager,
                            db=self.db_manager)
        q_delete.exec()

    def delete_images(self):
        self.logger.info("Click 'Delete Image'")

        if len(self.tW_images.selectedItems()):
            rows = set()
            for item in self.tW_images.selectedItems():
                rows.add(item.row())
            self.statusbar.showMessage(f"{len(rows)} 개의 이미지 삭제 요청")
            q_delete = ImageDeleteDialog(self,
                                         image_num=len(rows),
                                         weed=self.weed_manager,
                                         db=self.db_manager)
            q_delete.exec()
        else:
            self.statusbar.showMessage("이미지를 삭제하려면 1개 이상의 이미지를 선택해야합니다.")
        self.cur_image_idx = -1

    def add_label_field(self):
        self.logger.info("Click 'add_label_field'")

        add_label_dialog = AddLabelDialog(self, dataset_id=self.cur_dataset_idx, db=self.db_manager)
        add_label_dialog.show()

    def delete_label_field(self):
        self.logger.info("Click 'delete_label_field'")

        delete_label_dialog = DeleteLabelDialog(self, label_info=self.cur_label_fields, db=self.db_manager)
        delete_label_dialog.show()

    def get_upper_image(self):
        self.logger.info("Click 'upper image'")
        if not self.tW_images.selectedItems():
            self.tW_images.selectRow(0)
            self.draw_image(self.tW_images.item(0, 0))
        else:
            idx = self.tW_images.selectedIndexes()[0].row()
            idx = max(idx-1, 0)
            self.tW_images.selectRow(idx)
            self.draw_image(self.tW_images.item(idx, 0))

    def get_lower_image(self):
        self.logger.info("Click 'lower image'")
        if not self.tW_images.selectedItems():
            self.tW_images.selectRow(0)
            self.draw_image(self.tW_images.item(0, 0))
        else:
            num_row = self.tW_images.rowCount()
            idx = self.tW_images.selectedIndexes()[0].row()
            idx = min(idx + 1, num_row - 1)
            self.tW_images.selectRow(idx)
            self.draw_image(self.tW_images.item(idx, 0))

    def draw_dataset(self):
        ds = self.db_manager.read_dataset()

        for d in ds:
            ds_name = d[1]
            wg = ImageTabInnerWidget(self)
            wg.newShape.connect(self.draw_new_box_label)
            wg.selectionChanged.connect(self.shape_selection_changed)
            self.tW_img.addTab(wg, ds_name)

        self.cur_tab_idx = self.tW_img.currentIndex()
        self.cur_tab_name = self.tW_img.tabText(self.cur_tab_idx)
        self.cur_inner_tab = self.tW_img.currentWidget()
        self.logger.info(f"Success drawing datasets - Current tab index, name: {self.cur_tab_idx}-{self.cur_tab_name}")

    def draw_image_list_widget(self):
        # get current tab dataset_id
        ret = self.db_manager.read_dataset_detail(self.cur_tab_name)
        if ret:
            dataset_id = ret[0][0]
            self.cur_dataset_idx = dataset_id

            images = self.db_manager.read_image_data_by_dataset_id(dataset_id)
            self.tW_images.draw_image_list(images)

            self.logger.info(f"Success drawing image_list - Current tab index, dataset_id, image_len: "
                             f"{self.cur_tab_idx}-{dataset_id}, {len(images)} images")

    def draw_image(self, item: QTableWidgetItem):
        img_idx = self.tW_images.item(item.row(), 0).text()
        img_name = self.tW_images.item(item.row(), 1).text()
        image_fid = self.tW_images.fid_dict[int(img_idx)]

        img = self.weed_manager.get_image(fid=image_fid)

        self.cur_inner_tab.pos_click = []

        # self.cur_inner_tab.bg_label.bg_img = img
        self.cur_inner_tab.set_pixmap(img.toqpixmap(), scale=True)
        # self.cur_inner_tab.bg_label.boxes_rect = []
        self.cur_image_idx = img_idx

        # clear label field
        self.clear_img_label_captions()
        self.clear_img_label_cls()
        self.clear_boxes_label_box()
        # clear boxes-cap label
        # clear boxes-cls label

        # Draw label field
        self.draw_cur_img_caption_label()
        self.draw_cur_img_classification_label()
        self.draw_cur_boxes_box_label()

        self.statusbar.showMessage(f"Draw Image - Current tab index: {img_idx}({img_name})")

    def change_tab(self, index):
        self.cur_tab_idx = index
        self.cur_tab_name = self.tW_img.tabText(index)
        self.cur_inner_tab = self.tW_img.currentWidget()

        self.draw_image_list_widget()
        self.clean_label_field()
        self.draw_label_field()

        self.logger.info(f"Success changing tab index, name: {index}-{self.cur_tab_name}")

    def clean_label_field(self):
        while self.vlo_img_label_field.count() > 0:
            b = self.vlo_img_label_field.takeAt(0)
            w = b.widget()
            w.deleteLater()
        while self.vlo_box_label_field.count() > 0:
            b = self.vlo_box_label_field.takeAt(0)
            w = b.widget()
            w.deleteLater()

    def draw_label_field(self):
        self.cur_label_fields = []
        self.cur_label_fields_class = {}
        self.cur_label_fields_idx_dict = {}

        self.lb_image_caps = []
        self.lb_image_cls = []
        self.lb_boxes_box = []

        rets = self.db_manager.read_label_field_by_dataset_id(self.cur_dataset_idx)
        image_cap, image_cls = [], []
        boxes_box, boxes_cap, boxes_cls = [], [], []

        label_field_id = []
        for ret in rets:
            label_field_id.append(ret[0])
            field_name = ret[1]
            # dataset_id = ret[2]       # self.cur_dataset_idx
            data_format = ret[3]
            data_type = ret[4]
            is_duplicate = ret[5]
            classes = json.loads(ret[6])

            if data_format == 0 and data_type == 0:     # boxes-box
                self.cur_label_fields.append([ret[0], 'boxes-box'])
                boxes_box.append(classes)
            elif data_format == 0 and data_type == 1:   # boxes-cap
                self.cur_label_fields.append([ret[0], field_name])
                boxes_cap.append(field_name)
            elif data_format == 0 and data_type == 2:   # boxes-cls
                self.cur_label_fields.append([ret[0], field_name])
                boxes_cls.append([field_name, is_duplicate, classes])
            elif data_format == 1 and data_type == 1:   # image-cap
                self.cur_label_fields.append([ret[0], field_name])
                image_cap.append(field_name)
            elif data_format == 1 and data_type == 2:   # image-cls
                self.cur_label_fields.append([ret[0], field_name])
                image_cls.append([field_name, is_duplicate, classes])

        for label_field in self.cur_label_fields:
            self.cur_label_fields_idx_dict[label_field[1]] = label_field[0]

        # image-cap
        for f_name in image_cap:
            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            q_ptext.textChanged.connect(self.is_valid_change_img_caption)
            self.vlo_img_label_field.addWidget(q_ptext)
            self.lb_image_caps.append([f_name, q_ptext])

        # image-cls
        for data in image_cls:
            f_name, is_duplicate, classes = data

            if f_name not in self.cur_label_fields_class:
                self.cur_label_fields_class[f_name] = {}
            for idx, label_name in classes.items():
                self.cur_label_fields_class[f_name][label_name] = idx

            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate,
                                            clicked_callback=self.is_valid_change_img_cls)
            self.vlo_img_label_field.addWidget(group_box)
            self.lb_image_cls.append([f_name, group_box])

        # boxes-box
        for classes in boxes_box:

            if 'boxes-box' not in self.cur_label_fields_class:
                self.cur_label_fields_class['boxes-box'] = {}
            for idx, label_name in classes.items():
                self.cur_label_fields_class['boxes-box'][label_name] = idx

            text = ""
            for idx, cls_name in classes.items():
                text += f"{idx}: {cls_name} / "
            q_label = create_label(self,
                                   text=text,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="color: blue; font-weight: bold;")
            self.vlo_box_label_field.addWidget(q_label)
            self.lb_boxes_box = [self.cur_label_fields_idx_dict['boxes-box'], self.lw_labels]

        # boxes-cap
        for f_name in boxes_cap:
            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_box_label_field.addWidget(q_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            self.vlo_box_label_field.addWidget(q_ptext)

        # boxes-cls
        for data in boxes_cls:
            f_name, is_duplicate, classes = data

            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_box_label_field.addWidget(q_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate)
            self.vlo_box_label_field.addWidget(group_box)

        self.logger.info(f"Success drawing label_field - label_field_id: {label_field_id}")

    def draw_one_label_field(self, db_id, data_format, data_type, field_name, is_duplicate, classes):
        # image-cap
        if data_format == 1 and data_type == 1:
            q_label = create_label(self,
                                   text=field_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            q_ptext.textChanged.connect(self.is_valid_change_img_caption)
            self.vlo_img_label_field.addWidget(q_ptext)
            self.lb_image_caps.append([field_name, q_ptext])

        # image-cls
        elif data_format == 1 and data_type == 2:
            q_label = create_label(self,
                                   text=field_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate,
                                            clicked_callback=self.is_valid_change_img_cls)
            self.vlo_img_label_field.addWidget(group_box)
            self.lb_image_cls.append([field_name, group_box])

        # boxes-box
        elif data_format == 0 and data_type == 0:
            field_name = 'boxes-box'
            text = ""
            for idx, cls_name in classes.items():
                text += f"{idx}: {cls_name} "
            q_label = create_label(self,
                                   text=text,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="color: blue; font-weight: bold;")
            self.vlo_box_label_field.addWidget(q_label)

        # boxes-cap
        elif data_format == 0 and data_type == 1:
            q_label = create_label(self,
                                   text=field_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_box_label_field.addWidget(q_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            self.vlo_box_label_field.addWidget(q_ptext)

        # boxes-cls
        elif data_format == 0 and data_type == 2:
            q_label = create_label(self,
                                   text=field_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_box_label_field.addWidget(q_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate)
            self.vlo_box_label_field.addWidget(group_box)

        self.cur_label_fields.append([db_id, field_name])
        self.cur_label_fields_idx_dict[field_name] = db_id
        self.logger.info(f"Success add label_field - label_field_id: {db_id}")

    def is_valid_change_img_caption(self):
        if self.cur_image_idx == -1:
            for cap_data in self.lb_image_caps:
                plain_text = cap_data[1]
                if len(plain_text.toPlainText()):
                    msgBox = QMessageBox(text="이미지 캡션 라벨은 이미지를 선택 후 입력할 수 있습니다.")
                    msgBox.exec()
                    self.clear_img_label_captions()
        else:
            return

    def is_valid_change_img_cls(self):
        if self.cur_image_idx == -1:
            for cls_data in self.lb_image_cls:
                group_box = cls_data[1]
                for c in group_box.children():
                    if type(c) in [QRadioButton, QCheckBox]:
                        if c.isChecked():
                            msgBox = QMessageBox(text="이미지 클래스 라벨은 이미지 선택 후 입력 가능합니다.")
                            msgBox.exec()
                            self.clear_img_label_cls()
        else:
            return

    def clear_img_label_captions(self):
        for cap_data in self.lb_image_caps:
            plain_text = cap_data[1]
            plain_text.clear()

    def clear_img_label_cls(self):
        for cls_data in self.lb_image_cls:
            group_box = cls_data[1]
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    c.setAutoExclusive(False)
                    c.setChecked(False)
                    if isinstance(c, QRadioButton):
                        c.setAutoExclusive(True)
                    else:  # checkbox
                        c.setAutoExclusive(False)

    def clear_boxes_label_box(self):
        # List widget clear
        self.lw_labels.clear()

        # Image tab widget clear
        self.cur_inner_tab.reset_label()

        # parameter clear
        self.lb_items_to_shapes = {}
        self.lb_shapes_to_items = {}

    def save_labels(self):
        # 현재 이미지, 라벨 필드 목록
        # print(self.cur_image_idx, self.cur_label_fields)
        # print(self.cur_label_fields_idx_dict)

        # DB에서 현재 데이터셋 필드 조회

        # Delete entire label in current image
        self.db_manager.delete_label_data_by_image_data_id(self.cur_image_idx)

        # Save image-cap label
        self.save_img_caption_label()

        # Save image-cls label
        self.save_img_classification_label()

        # Save boxes-box label
        self.save_boxes_box_label()

        # 박스 - 캡션

        # 박스 - 클래스

    def save_img_caption_label(self):
        for cap_label in self.lb_image_caps:
            field_name, plain_text = cap_label
            caption_text = plain_text.toPlainText()
            label_field_id = self.cur_label_fields_idx_dict[field_name]

            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_idx,
                label_field_id=label_field_id,
                is_box=0,
                caption=caption_text
            )

            self.logger.info(f"Success save image-caption label_data_id: {lastrowid}")

    def draw_cur_img_caption_label(self):
        fields = []
        for cap_label in self.lb_image_caps:
            field_name, plain_text = cap_label
            label_field_idx = self.cur_label_fields_idx_dict[field_name]
            fields.append(field_name)
            ret = self.db_manager.read_label_data(
                image_data_id=self.cur_image_idx,
                label_field_id=label_field_idx
            )
            if ret:
                caption_text = ret[0][7]
                plain_text.setPlainText(caption_text)

        self.logger.info(f"load {self.cur_image_idx} idx image caption fields: {fields}")

    def save_img_classification_label(self):
        field_idx_class = []
        for cls_label in self.lb_image_cls:
            field_name, group_box = cls_label
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    if c.isChecked():
                        field_idx = self.cur_label_fields_idx_dict[field_name]
                        label_cls = self.cur_label_fields_class[field_name][c.text()]
                        field_idx_class.append([field_idx, label_cls])
                else:   # hlo
                    continue
        for cls_data in field_idx_class:
            label_field_id, cls = cls_data
            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_idx,
                label_field_id=label_field_id,
                is_box=0,
                cls=cls
            )

            self.logger.info(f"Success save image-classes label_data_id: {lastrowid}")

    def draw_cur_img_classification_label(self):
        fields = []
        for cls_label in self.lb_image_cls:
            field_name, group_box = cls_label
            fields.append(field_name)
            label_field_idx = self.cur_label_fields_idx_dict[field_name]
            rets = self.db_manager.read_label_data(
                image_data_id=self.cur_image_idx,
                label_field_id=label_field_idx
            )
            check_label = []
            for ret in rets:
                cls = ret[6]
                for label_name, label_idx in self.cur_label_fields_class[field_name].items():
                    if int(label_idx) == cls:
                        check_label.append(label_name)
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    if c.text() in check_label:
                        c.setChecked(True)

        self.logger.info(f"load {self.cur_image_idx} idx image-class fields: {fields}")

    def save_boxes_box_label(self):
        boxes = []
        label_field_idx, list_widget = self.lb_boxes_box

        for box_shape, list_widget_item in self.lb_shapes_to_items.items():
            points = box_shape.points
            xyxy = get_xyxy(points)
            pixmap_size = self.cur_inner_tab.pixmap.size()
            rel_xyxy = xyxy_to_rel(xyxy, pixmap_size)
            cls = self.cur_label_fields_class['boxes-box'][list_widget_item.text()]

            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_idx,
                label_field_id=label_field_idx,
                is_box=1,
                coord=str(list(rel_xyxy)),
                cls=cls
            )
            boxes.append(lastrowid)

        self.logger.info(f"Success save {len(boxes)} boxes-box ids: {boxes}")

    def draw_cur_boxes_box_label(self):
        label_field_idx, list_widget = self.lb_boxes_box
        tab_widget = self.cur_inner_tab

        rets = self.db_manager.read_label_data(
            image_data_id=self.cur_image_idx,
            label_field_id=label_field_idx
        )
        for ret in rets:
            is_box = ret[4]
            if is_box != 1:
                continue
            elif is_box == 1:
                coord = eval(ret[5])
                cls = ret[6]
                cls_name = None
                for label_name, label_idx in self.cur_label_fields_class['boxes-box'].items():
                    if int(label_idx) == cls:
                        cls_name = label_name
                        break

                x1, y1, x2, y2 = rel_to_xyxy(coord, tab_widget.pixmap.size())
                _box = Shape(label=cls_name)
                _box.add_point(QPointF(x1, y1))
                _box.add_point(QPointF(x2, y1))
                _box.add_point(QPointF(x2, y2))
                _box.add_point(QPointF(x1, y2))
                tab_widget.shapes.append(_box)
                g_color = generate_color_by_text(cls_name)
                shape = self.cur_inner_tab.set_last_label(cls_name, line_color=g_color, fill_color=g_color)
                self.add_box_label(shape)

    def draw_new_box_label(self):
        # box 클래스 라벨이 없을 때 예외 다이어로그 처리
        ret = self.db_manager.read_label_field_by_dataset_id(self.cur_dataset_idx)
        is_exist_box_label = False
        classes = None
        for r in ret:
            data_subject, data_type = r[3], r[4]
            if data_subject == 0 and data_type == 0:
                is_exist_box_label = True
                classes = json.loads(r[6])

        if is_exist_box_label is False:
            msgBox = QMessageBox(text="박스형 라벨 필드가 존재하지 않습니다.")
            msgBox.exec()
            self.cur_inner_tab.reset_all_lines()

        # 있다면
        text = classes[list(classes.keys())[0]]     # default_class_name: 0번 클래스 이름
        g_color = generate_color_by_text(text)
        shape = self.cur_inner_tab.set_last_label(text, line_color=g_color, fill_color=g_color)
        shape.set_class(0)
        self.add_box_label(shape)
        if self.beginner():
            self.cur_inner_tab.set_editing(True)
        # else:
        #     pass

    def delete_selected_boxes_box_label(self):
        shape = self.cur_inner_tab.delete_selected_shape()
        if shape is None:
            return
        item = self.lb_shapes_to_items[shape]
        self.lw_labels.takeItem(self.lw_labels.row(item))
        del self.lb_shapes_to_items[shape]
        del self.lb_items_to_shapes[item]
        self.logger.info(f"Delete box label: {shape.label}")

    def keyPressEvent(self, event):
        if Qt.Key.Key_Comma == event.key():
            self.get_upper_image()
        elif Qt.Key.Key_Period == event.key():
            self.get_lower_image()

        if self.cur_inner_tab.selected_shape is not None:
            shape = self.cur_inner_tab.selected_shape
            if self._is_change_box_class is False and event.key() == Qt.Key.Key_Alt:
                self._is_change_box_class = True
                self.statusbar.showMessage("Enable to change class number")
                return
            if self._is_change_box_class is True and event.text().isdigit():
                press_num = event.text()
                self._change_box_class.append(press_num)
                _change_cls = "".join(self._change_box_class)
                if _change_cls in list(self.cur_label_fields_class['boxes-box'].values()):
                    shape.set_class(int(_change_cls))
                    for cls_name, cls_idx in self.cur_label_fields_class['boxes-box'].items():
                        if cls_idx == _change_cls:
                            shape.label = cls_name
                            break
                    item = self.lb_shapes_to_items[shape]
                    item.setText(shape.label)
                    item.setBackground(generate_color_by_text(shape.label))
                    self.cur_inner_tab.repaint()
                    self.statusbar.showMessage(f"Update to change class number: {_change_cls, shape.label}")

    def keyReleaseEvent(self, event):
        if self._is_change_box_class is True:
            if event.key() == Qt.Key.Key_Alt:
                self._is_change_box_class = False
                self._change_box_class = []
                self.statusbar.showMessage("Finish to change class number")

    def current_item(self):
        items = self.lw_labels.selectedItems()
        if items:
            return items[0]
        return None

    def set_create_mode(self):
        self.cur_inner_tab.set_editing(False)
        # self.actionCreate_Mode.setEnabled(False)
        # self.actionEdit_Mode.setEnabled(True)

    def set_edit_mode(self):
        self.cur_inner_tab.set_editing(True)
        # self.actionCreate_Mode.setEnabled(True)
        # self.actionEdit_Mode.setEnabled(False)
        self.label_selection_changed()

    def shape_selection_changed(self):
        if self._no_selection_slot:
            self._no_selection_slot = False
        else:
            shape = self.cur_inner_tab.selected_shape
            if shape:
                self.lb_shapes_to_items[shape].setSelected(True)
            else:
                self.lw_labels.clearSelection()

    def label_selection_changed(self):
        item = self.current_item()
        if item and self.cur_inner_tab.is_editing():
            self._no_selection_slot = True
            shape = self.lb_items_to_shapes[item]
            self.cur_inner_tab.select_shape(shape)

    def beginner(self):
        return self._beginner

    def add_box_label(self, shape):
        shape.paint_label = True
        item = BoxQListWidgetItem(shape.label)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)
        item.setBackground(generate_color_by_text(shape.label))
        self.lb_items_to_shapes[item] = shape
        self.lb_shapes_to_items[shape] = item
        self.lw_labels.addItem(item)
        # for action in self.actions.onShapesPresent:
        #     action.setEnabled(True)
        # self.update_combo_box()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # init config & logger
    set_config('./configs/config.yaml')
    _cfg = get_config()

    init_logger(_cfg)
    _logger = get_logger()

    window = MainWindow(cfg=_cfg, logger=_logger)
    window.show()

    sys.exit(app.exec())
