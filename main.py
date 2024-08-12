# This Python file uses the following encoding: utf-8
import logging
import os
import sys
import json
import yaml
import time
import random
import cv2
from datetime import datetime

from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QPlainTextEdit,
                               QMessageBox, QRadioButton, QCheckBox, QDialog)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from utils.qt import (create_label, create_button_group, generate_color_by_text, get_xyxy, xyxy_to_rel, rel_to_xyxy,
                      get_dir_dialog, get_file_dialog)
from utils.coord import absxyxy_to_relxyxy
from utils.checks import is_empty
from ui.ui_mainwindow import Ui_MainWindow
from core.database import DBManager
from core.weedfs import SeaWeedFS
from core.obj_detector import ObjectDetector
from core.qt.inner_tab import ImageTabInnerWidget
from core.qt.simple_dialog import (DatasetDeleteDialog, ImagesDeleteDialog, LabelsFieldDeleteDialog,
                                   DetectionLabelsCreateDialog)
from core.qt.create_dataset_dialog import CreateDatasetDialog
from core.qt.add_label_field_dialog import AddLabelFieldDialog
from core.qt.edit_label_field_dialog import EditLabelFieldDialog
from core.qt.export_dialog import ExportDialog
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
        self.dataset_dict_name_to_idx = {}
        self.cur_dataset_db_idx = -1
        self.cur_dataset_name = None
        self.prev_image_row_idx = None
        self.cur_image_row_idx = None
        self.cur_image_db_idx = -1
        self.cur_inner_tab = None
        self.cur_inner_tab_name = None
        self.cur_inner_tab_ui_idx = -1

        self.is_autosave = False
        self.is_label_change = False

        self.detector = None

        # label fields
        self.label_fields_list_idx_name = []
        self.label_fields_dict_name_to_idx = {}
        self.label_fields_dict_idx_to_name = {}
        self.label_field_name_dict_classname_to_idx = {}

        self.label_field_image_caps = []
        self.label_field_image_cls = []
        self.label_field_boxes_box = []
        self.bbox_items_to_shapes = {}
        self.bbox_shapes_to_items = {}
        self.bbox_new_shapes_to_items = {}

        # Inner param
        self._no_selection_slot = False
        self._is_change_box_class = False
        self._change_box_class = []

        # init drawing
        self.draw_ui_dataset_inner_tab_widget()
        self.draw_ui_image_list()
        self.clear_ui_label_fields()
        self.draw_ui_label_fields()

        # Signal and Slot
        # Header
        self.checkbox_autosave.stateChanged.connect(self.change_autosave_checkbox)
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.tB_header_uploadDir.clicked.connect(self.upload_dir)
        self.tB_header_uploadImage.clicked.connect(self.upload_images)
        self.tB_header_delDataset.clicked.connect(self.delete_dataset)
        self.tB_header_delSelectedImage.clicked.connect(self.delete_images)

        # Menubar - File
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)
        self.actionUpload_folder.triggered.connect(self.upload_dir)
        self.actionUpload_Image.triggered.connect(self.upload_images)
        self.actionDelete_Dataset.triggered.connect(self.delete_dataset)
        self.actionDelete_Selected_Image.triggered.connect(self.delete_images)

        self.actionSave_label.triggered.connect(self.save_db_labels)

        # Menubar - Data
        self.actionCreate_Mode.triggered.connect(self.set_create_mode)
        self.actionEdit_Mode.triggered.connect(self.set_edit_mode)
        self.actionSelect_up_image.triggered.connect(self.select_upper_image)
        self.actionSelect_down_image.triggered.connect(self.select_lower_image)
        self.actionDelete_selected_box.triggered.connect(self.clear_selected_bbox_label)

        # Menubar - infer
        self.actionObject_Detection_for_entire_images.triggered.connect(
            lambda x: self.create_box_label_by_detection_entire_images(True))
        self.actionObject_Detection_for_selected_images.triggered.connect(
            lambda x: self.create_box_label_by_detection_selected_images(True))
        self.actionObject_Detection_for_current_image.triggered.connect(
            lambda x: self.create_box_label_by_detection_current_image(True))
        self.actionObject_Detection_for_entire_images_without_removing.triggered.connect(
            lambda x: self.create_box_label_by_detection_entire_images(False))
        self.actionObject_Detection_for_selected_images_without_removing.triggered.connect(
            lambda x: self.create_box_label_by_detection_selected_images(False))
        self.actionObject_Detection_for_current_image_without_removing.triggered.connect(
            lambda x: self.create_box_label_by_detection_current_image(False))

        # Menubar - Export
        self.actionExport_YOLO_detect_dataset.triggered.connect(self.export_yolo_detection_dataset)

        # ImageList
        self.image_list_widget.itemClicked.connect(self.draw_image_item)
        self.tB_img_up.clicked.connect(self.select_upper_image)
        self.tB_img_down.clicked.connect(self.select_lower_image)
        self.tB_img_del.clicked.connect(self.delete_images)

        # BBoxList
        self.bbox_listwidget.itemActivated.connect(self.label_selection_changed)
        self.bbox_listwidget.itemSelectionChanged.connect(self.label_selection_changed)
        self.bbox_listwidget.itemChanged.connect(self.label_item_changed)

        # Tab Widget
        self.tab_widget.currentChanged.connect(self.select_inner_tab_widget)

        # Label Field
        self.pB_label_add.clicked.connect(self.create_label_field)
        self.pB_label_edit.clicked.connect(self.edit_label_field)
        self.pB_label_del.clicked.connect(self.delete_label_field)

        self.logger.info("Success initializing MainWindow")

    def create_dataset(self):
        self.logger.info("클릭 - 데이터 셋 생성")
        dialog = CreateDatasetDialog(self)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("데이터 셋 생성 취소")
            return
        dataset_name = dialog.le_dataset_name.text()
        dataset_type = dialog.get_dataset_type()
        dataset_desc = dialog.te_ds_desc.toPlainText()

        # check dataset name is empty
        if is_empty(dataset_name) is True:
            msgBox = QMessageBox(text="데이터 셋 이름은 공백이 될 수 없습니다.")
            msgBox.exec()
            self.logger.warning("데이터 셋 이름 공백 문제 발생")
            return
        # check dataset name is duplicated
        res = self.db_manager.read_dataset_by_name(dataset_name)
        if len(res) != 0:
            msgBox = QMessageBox(text="이미 존재하는 데이터 셋 이름입니다.")
            msgBox.exec()
            self.logger.warning("데이터 셋 이름 중복 문제 발생")
            return

        # insert DB
        try:
            lastrowid = self.db_manager.create_dataset(dataset_name, dataset_type, dataset_desc)
            msgBox = QMessageBox(text="데이터 셋 생성에 성공하였습니다.")
            msgBox.exec()
        except Exception as e:
            msgBox = QMessageBox(text=f"데이터 셋 생성에 실패했습니다: {e}")
            msgBox.exec()
            self.logger.error(f"데이터 셋 생성 에러: {e}")
            return
        self.dataset_dict_name_to_idx[dataset_name] = lastrowid

        # Draw UI
        widget = ImageTabInnerWidget(self)
        widget.newShape.connect(self.draw_new_bbox_label)
        widget.selectionChanged.connect(self.shape_selection_changed)
        self.tab_widget.addTab(widget, dataset_name)

        self.logger.info(f"데이터 셋 생성: {dataset_name} / 타입-{dataset_type} / 설명-{dataset_desc}")

    def delete_dataset(self):
        self.logger.info("클릭 - 데이터 셋 삭제")
        dataset_name = self.cur_inner_tab_name
        dialog = DatasetDeleteDialog(self, dataset_name=dataset_name)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("데이터 셋 삭제 취소")
            return

        num_img = len(self.image_list_widget.fid_dict)
        # Delete All images in weedfs
        for db_idx, img_fid in self.image_list_widget.fid_dict.items():
            self.weed_manager.delete_file(fid=img_fid)

        # delete DB with delete cascade
        try:
            self.db_manager.delete_dataset_by_name(dataset_name)
            msgBox = QMessageBox(text="데이터 셋 삭제를 완료하였습니다.")
            msgBox.exec()
        except Exception as e:
            msgBox = QMessageBox(text=f"데이터 셋 삭제에 실패했습니다: {e}")
            msgBox.exec()
            self.logger.error(f"데이터 셋 삭제 에러: {e}")
            return

        # Update UI
        self.tab_widget.removeTab(self.tab_widget.currentIndex())
        del self.dataset_dict_name_to_idx[dataset_name]

        self.logger.info(f"데이터 셋 삭제: {dataset_name} / 지워진 이미지 수: {num_img}")

    def upload_dir(self):
        self.logger.info("클릭 - 업로드 디렉토리")
        dir_dialog = get_dir_dialog(self)

        dirname = dir_dialog.getExistingDirectory(
            parent=self,
            caption='Select Directory',
            dir=""
        )
        if not dirname:
            self.logger.info("이미지 디렉토리 업로드 취소")
            return
        else:
            file_names = []
            for file in sorted(os.listdir(dirname)):
                basename, ext = os.path.splitext(file)
                file_path = os.path.join(dirname, file)
                if ext.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                    file_names.append(file_path)
            for f_idx, filename in enumerate(file_names):
                self.statusbar.showMessage(f"Upload image ... ({f_idx + 1}/{len(file_names)})")
                self.upload_image(filename)
            self.logger.info("이미지 디렉토리 업로드 완료")
            self.statusbar.showMessage("이미지 디렉토리 업로드 완료")

    def upload_images(self):
        self.logger.info("클릭 - 이미지 업로드")
        file_dialog = get_file_dialog(self, multiple_files=True)

        fileNames = file_dialog.getOpenFileNames(
            parent=self,
            caption="Open Image",
            dir="",
            filter="Image Files (*.png *.jpg *.jpeg *.bmp)",
        )
        file_names, filters = fileNames
        if not file_names:
            self.logger.info("이미지 업로드 취소")
            return
        else:
            for f_idx, filename in enumerate(file_names):
                self.statusbar.showMessage(f"Upload image ... ({f_idx+1}/{len(file_names)})")
                self.upload_image(filename)
            self.logger.info("이미지 업로드 완료")
            self.statusbar.showMessage(f"이미지 업로드 완료")

    def upload_image(self, filepath, weed=True, db=True, ui=True):
        # Upload seaweed
        if weed is True:
            ret = self.weed_manager.put_image_collection(image=filepath, filename=filepath)

            # Upload DB
            if db is True:
                idx = self.db_manager.create_image_data(
                    dataset_id=self.cur_dataset_db_idx,
                    filename=ret['filename'],
                    image_fid=ret['fid'],
                    image_url=ret['url'],
                    width=ret['width'],
                    height=ret['height']
                )

                # Update UI: left image table list
                if ui is True:
                    self.image_list_widget.add_image_list(idx, ret['filename'], ret['fid'], ret['url'])

    def delete_images(self):
        self.logger.info("클릭 - 선택 이미지 삭제")

        if len(self.image_list_widget.selectedItems()) == 0:
            msg = "이미지를 삭제하려면 1개 이상의 이미지를 선택해야합니다."
            self.statusbar.showMessage(msg)
            msgBox = QMessageBox(text=msg)
            msgBox.exec()
        else:
            # Get Selected image number and index
            rows = set()
            for item in self.image_list_widget.selectedItems():
                img_db_idx = int(self.image_list_widget.item(item.row(), 0).text())
                rows.add(img_db_idx)
            self.statusbar.showMessage(f"{len(rows)} 개의 이미지 삭제 요청")
            dialog = ImagesDeleteDialog(self, image_num=len(rows))
            ret = dialog.exec()
            if ret == QDialog.DialogCode.Rejected:
                self.logger.info("선택 이미지 삭제 취소")
                return
            try:
                for img_db_idx in rows:
                    img_fid = self.image_list_widget.fid_dict[img_db_idx]

                    # Delete selected iamges in weedfs
                    ret = self.weed_manager.delete_file(fid=img_fid)

                    # Delete in DB
                    if ret is True:
                        self.db_manager.delete_image_data_by_image_id(img_db_idx)
                        self.statusbar.showMessage(f"Success delete image {img_db_idx}")
                msgBox = QMessageBox(text="선택 이미지 삭제를 완료하였습니다.")
                msgBox.exec()
            except Exception as e:
                msgBox = QMessageBox(text=f"선택 이미지 삭제에 실패했습니다: {e}")
                msgBox.exec()
                self.logger.error(f"선택 이미지 삭제 에러: {e}")
                return

            # Update UI
            include = False if len(rows) == 1 else True
            self.clear_ui_image_list(include_row=include)
            self.draw_ui_image_list()
            self.clear_ui_image()
            self.clear_ui_label_data()

            # Process special case
            if len(rows) == 1:
                self.image_list_widget.selectRow(self.prev_image_row_idx)

            self.logger.info(f"선택 이미지 삭제 - 지워진 이미지 수: {len(rows)}")

    def delete_selected_images_labels(self):
        # 현 화면 라벨 UI 정리
        self.clear_ui_label_data()
        pass

    def delete_current_image_labels(self):
        # 현 화면 라벨 UI 정리
        self.clear_ui_label_data()
        pass

    def delete_labels(self):
        # 바운딩 박스 DB 삭제

        # 이미지 라벨 DB 삭제

        # 박스 라벨 DB 삭제
        pass

    def clear_ui_image(self):
        """탭 위젯의 이미지 픽스맵 초기화 및 좌측 이미지 목록의 이미지 선택 초기화

        Returns:

        """
        self.cur_inner_tab.pixmap = QPixmap()
        self.image_list_widget.clearSelection()
        self.cur_image_db_idx = -1

    def clear_ui_label_data(self):
        """우측 박스 목록, 박스 관련 라벨, 이미지 관련 라벨 초기화

        Returns:

        """
        self.clear_ui_bbox_label_data()
        self.clear_ui_img_label_data()
        self.clear_ui_box_label_data()

    def clear_ui_bbox_label_data(self):
        # List widget clear
        self.bbox_listwidget.clear()

        # Image tab widget clear
        self.cur_inner_tab.reset_label()

        # parameter clear
        self.bbox_items_to_shapes = {}
        self.bbox_shapes_to_items = {}

    def clear_ui_box_label_data(self):
        # self.clear_box_label_captions()
        # self.clear_box_label_cls()
        pass

    def clear_ui_img_label_data(self):
        self.clear_ui_img_label_captions()
        self.clear_ui_img_label_cls()

    def clear_ui_img_label_captions(self):
        for cap_data in self.label_field_image_caps:
            plain_text = cap_data[1]
            plain_text.clear()

    def clear_ui_img_label_cls(self):
        for cls_data in self.label_field_image_cls:
            group_box = cls_data[1]
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    c.setAutoExclusive(False)
                    c.setChecked(False)
                    if isinstance(c, QRadioButton):
                        c.setAutoExclusive(True)
                    else:  # checkbox
                        c.setAutoExclusive(False)

    def clear_ui_image_list(self, include_row=True):
        self.image_list_widget.clear_image_list()
        self.image_list_widget.clearSelection()
        if include_row:
            self.prev_image_row_idx = None
            self.cur_image_row_idx = None

    def clear_ui_label_fields(self):
        self.clear_ui_img_label_fields()
        self.clear_ui_box_label_fields()

        self.label_fields_list_idx_name = []
        self.label_fields_dict_name_to_idx = {}
        self.label_fields_dict_idx_to_name = {}
        self.label_field_name_dict_classname_to_idx = {}

        self.label_field_image_caps = []
        self.label_field_image_cls = []
        self.label_field_boxes_box = []

    def clear_ui_img_label_fields(self):
        while self.vlo_img_label_field.count() > 0:
            b = self.vlo_img_label_field.takeAt(0)
            w = b.widget()
            w.deleteLater()

    def clear_ui_box_label_fields(self):
        while self.vlo_box_label_field.count() > 0:
            b = self.vlo_box_label_field.takeAt(0)
            w = b.widget()
            w.deleteLater()

    def draw_ui_label_fields(self):
        rets = self.db_manager.read_label_field_by_dataset_id(self.cur_dataset_db_idx)
        image_cap, image_cls = [], []
        boxes_box, boxes_cap, boxes_cls = [], [], []

        for ret in rets:
            field_db_idx = ret[0]
            field_name = ret[1]
            # dataset_id = ret[2]       # self.cur_dataset_db_idx
            data_format = ret[3]
            data_type = ret[4]
            is_duplicate = ret[5]
            classes = json.loads(ret[6])

            if data_format == 0 and data_type == 0:     # boxes-box
                field_name = 'boxes-box'
                self.label_fields_list_idx_name.append([ret[0], 'boxes-box'])
                boxes_box.append(classes)
                if 'boxes-box' not in self.label_field_name_dict_classname_to_idx:
                    self.label_field_name_dict_classname_to_idx['boxes-box'] = {}
            elif data_format == 0 and data_type == 1:   # boxes-cap
                self.label_fields_list_idx_name.append([ret[0], field_name])
                boxes_cap.append(field_name)
            elif data_format == 0 and data_type == 2:   # boxes-cls
                self.label_fields_list_idx_name.append([ret[0], field_name])
                if field_name not in self.label_field_name_dict_classname_to_idx:
                    self.label_field_name_dict_classname_to_idx[field_name] = {}
                boxes_cls.append([field_name, is_duplicate, classes])
            elif data_format == 1 and data_type == 1:   # image-cap
                self.label_fields_list_idx_name.append([ret[0], field_name])
                image_cap.append(field_name)
            elif data_format == 1 and data_type == 2:   # image-cls
                self.label_fields_list_idx_name.append([ret[0], field_name])
                image_cls.append([field_name, is_duplicate, classes])
                if field_name not in self.label_field_name_dict_classname_to_idx:
                    self.label_field_name_dict_classname_to_idx[field_name] = {}

            self.label_fields_dict_name_to_idx[field_name] = field_db_idx
            self.label_fields_dict_idx_to_name[field_db_idx] = field_name

        # boxes-box
        for classes in boxes_box:
            field_name = 'boxes-box'
            for idx, label_name in classes.items():
                self.label_field_name_dict_classname_to_idx[field_name][label_name] = idx
            self.draw_ui_one_label_field(0, 0, field_name, 0, classes)
        # boxes-cap
        for field_name in boxes_cap:
            self.draw_ui_one_label_field(0, 1, field_name, 0, None)
        # boxes-cls
        for data in boxes_cls:
            field_name, is_duplicate, classes = data
            for idx, label_name in classes.items():
                self.label_field_name_dict_classname_to_idx[field_name][label_name] = idx
            self.draw_ui_one_label_field(0, 2, field_name, is_duplicate, classes)
        # image-cap
        for field_name in image_cap:
            self.draw_ui_one_label_field(1, 1, field_name, 0, None)
        # image-cls
        for data in image_cls:
            field_name, is_duplicate, classes = data
            for idx, label_name in classes.items():
                self.label_field_name_dict_classname_to_idx[field_name][label_name] = idx
            self.draw_ui_one_label_field(1, 2, field_name, is_duplicate, classes)

    def draw_ui_one_label_field(self, data_format, data_type, field_name, is_duplicate, classes):
        # boxes-box
        if data_format == 0 and data_type == 0:
            field_name = 'boxes-box'
            text = ""
            for idx, cls_name in classes.items():
                text += f"{idx}: {cls_name} "
            field_name_label = create_label(
                self,
                text=text,
                alignment=Qt.AlignmentFlag.AlignTop,
                stylesheet="color: blue; font-weight: bold;"
            )
            self.vlo_box_label_field.addWidget(field_name_label)
            self.label_field_boxes_box = [self.label_fields_dict_name_to_idx[field_name], self.bbox_listwidget]
        # boxes-cap
        elif data_format == 0 and data_type == 1:
            field_name_label = create_label(
                self,
                text=field_name,
                alignment=Qt.AlignmentFlag.AlignTop,
                stylesheet="font-weight: bold"
            )
            self.vlo_box_label_field.addWidget(field_name_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            self.vlo_box_label_field.addWidget(q_ptext)
            # self.label_field_boxes_cap = [self.label_fields_dict_name_to_idx[field_name], ?]
        # boxes-cls
        elif data_format == 0 and data_type == 2:
            field_name_label = create_label(
                self,
                text=field_name,
                alignment=Qt.AlignmentFlag.AlignTop,
                stylesheet="font-weight: bold"
            )
            self.vlo_box_label_field.addWidget(field_name_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate)
            self.vlo_box_label_field.addWidget(group_box)
            # self.label_field_boxes_cls = [self.label_fields_dict_name_to_idx[field_name], ?]
        # image-cap
        if data_format == 1 and data_type == 1:
            field_name_label = create_label(
                self,
                text=field_name,
                alignment=Qt.AlignmentFlag.AlignTop,
                stylesheet="font-weight: bold"
            )
            self.vlo_img_label_field.addWidget(field_name_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            q_ptext.textChanged.connect(self.is_valid_change_img_caption)
            self.vlo_img_label_field.addWidget(q_ptext)
            self.label_field_image_caps.append([field_name, q_ptext])
        # image-cls
        elif data_format == 1 and data_type == 2:
            field_name_label = create_label(
                self,
                text=field_name,
                alignment=Qt.AlignmentFlag.AlignTop,
                stylesheet="font-weight: bold"
            )
            self.vlo_img_label_field.addWidget(field_name_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate,
                                            clicked_callback=self.is_valid_change_img_cls)
            self.vlo_img_label_field.addWidget(group_box)
            self.label_field_image_cls.append([field_name, group_box])

        self.logger.info(f"라벨 필드 UI 그리기 - {field_name}")

    def draw_ui_label_data(self):
        self.draw_ui_bbox_label_data()
        self.draw_ui_img_label_data()
        self.draw_ui_box_label_data()

    def draw_ui_bbox_label_data(self):
        if not self.label_field_boxes_box:
            return

        label_field_db_idx, image_list_widget = self.label_field_boxes_box

        rets = self.db_manager.read_label_data(image_data_id=self.cur_image_db_idx, label_field_id=label_field_db_idx)

        for ret in rets:
            is_box, coord, cls = ret[4], eval(ret[5]), ret[6]
            if is_box != 1:
                continue
            else:
                cls_name = None
                for class_name, class_idx in self.label_field_name_dict_classname_to_idx['boxes-box'].items():
                    if int(class_idx) == cls:
                        cls_name = class_name
                        break

                # Shape and Item
                shape = self.create_bbox_shape(coord, cls_name, self.cur_inner_tab.pixmap.size())
                self.create_bbox_item(shape)

    def draw_ui_img_label_data(self):
        self.draw_ui_img_label_captions()
        self.draw_ui_img_label_cls()

    def draw_ui_box_label_data(self):
        self.draw_ui_box_label_captions()
        self.draw_ui_box_label_cls()

    def draw_ui_img_label_captions(self):
        field_names = []
        for image_caps in self.label_field_image_caps:
            field_name, plain_text = image_caps
            label_field_idx = self.label_fields_dict_name_to_idx[field_name]
            field_names.append(field_name)
            ret = self.db_manager.read_label_data(image_data_id=self.cur_image_db_idx, label_field_id=label_field_idx)
            if ret:
                caption_text = ret[0][7]
                plain_text.setPlainText(caption_text)

    def draw_ui_img_label_cls(self):
        field_names = []
        for image_cls in self.label_field_image_cls:
            field_name, group_box = image_cls
            field_names.append(field_name)
            label_field_idx = self.label_fields_dict_name_to_idx[field_name]
            rets = self.db_manager.read_label_data(image_data_id=self.cur_image_db_idx, label_field_id=label_field_idx)
            checked_label = []
            for ret in rets:
                cls = ret[6]
                for class_name, class_idx in self.label_field_name_dict_classname_to_idx[field_name].items():
                    if int(class_idx) == cls:
                        checked_label.append(class_name)
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    if c.text() in checked_label:
                        c.setChecked(True)

    def draw_ui_box_label_captions(self):
        pass

    def draw_ui_box_label_cls(self):
        pass

    def draw_ui_dataset_inner_tab_widget(self):
        rets = self.db_manager.read_dataset()

        for ret in rets:
            dataset_id = ret[0]
            dataset_name = ret[1]
            self.dataset_dict_name_to_idx[dataset_name] = dataset_id
            widget = ImageTabInnerWidget(self)
            widget.newShape.connect(self.draw_new_bbox_label)
            widget.selectionChanged.connect(self.shape_selection_changed)
            self.tab_widget.addTab(widget, dataset_name)

        self.cur_inner_tab_ui_idx = self.tab_widget.currentIndex()
        self.cur_inner_tab_name = self.tab_widget.tabText(self.cur_inner_tab_ui_idx)
        self.cur_dataset_name = self.cur_inner_tab_name
        self.cur_dataset_db_idx = self.dataset_dict_name_to_idx[self.cur_dataset_name]
        self.cur_inner_tab = self.tab_widget.currentWidget()
        self.logger.info(f"데이터 셋 탭 위젯 그리기 - index / name: {self.cur_inner_tab_ui_idx} / {self.cur_inner_tab_name}")

    def draw_ui_image_list(self):
        # get current tab iamges
        images = self.db_manager.read_image_data_by_dataset_id(self.cur_dataset_db_idx)
        self.image_list_widget.draw_image_list(images)

        self.logger.info(f"이미지 리스트 위젯 그리기 - {self.cur_inner_tab_ui_idx}번 탭 / {self.cur_dataset_name} / "
                         f"이미지 {len(images)}장")

    def draw_image_item(self, item: QTableWidgetItem):
        # Check prev image autosave
        self.check_autosave()

        img_db_idx = int(self.image_list_widget.item(item.row(), 0).text())
        img_filename = self.image_list_widget.item(item.row(), 1).text()
        img_fid = self.image_list_widget.fid_dict[img_db_idx]
        img_row_idx = item.row()

        img_pil = self.weed_manager.get_image(fid=img_fid)

        # draw
        self.cur_inner_tab.set_pixmap(img_pil.toqpixmap(), scale=True)
        self.cur_image_db_idx = img_db_idx
        if self.prev_image_row_idx is None:
            self.prev_image_row_idx = img_row_idx
        else:
            self.prev_image_row_idx = self.cur_image_row_idx
        self.cur_image_row_idx = img_row_idx

        # clear label field
        self.is_label_change = False
        self.clear_ui_label_data()

        # Draw label field
        self.draw_ui_label_data()
        self.cur_inner_tab.repaint()

        # Check selected row num
        num = self.image_list_widget.check_selected_row_num()

        self.statusbar.showMessage(f"이미지 그리기 - {img_db_idx}({img_filename}) / 선택된 이미지 수: {num}")
        self.logger.info(f"이미지 그리기 - {img_db_idx}({img_filename}) / 선택된 이미지 수: {num}")

    def create_label_field(self):
        self.logger.info("클릭 - 라벨 필드 추가")

        dialog = AddLabelFieldDialog(self, dataset_id=self.cur_dataset_db_idx, db=self.db_manager)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("라벨 필드 추가 취소")
            return
        elif ret == QDialog.DialogCode.Accepted:
            # label format - 0: boxes, 1: images
            label_format = 0
            if dialog.rb_boxes.isChecked():
                label_format = 0
            elif dialog.rb_image.isChecked():
                label_format = 1

            # label tpye - 0: box, 1: caption, 2: classification
            label_type = 0
            if dialog.rb_box.isChecked():
                label_type = 0
            elif dialog.rb_caption.isChecked():
                label_type = 1
            elif dialog.rb_cls.isChecked():
                label_type = 2

            # field name
            field_name = None
            if dialog.rb_caption.isChecked() or dialog.rb_cls.isChecked():
                field_name = dialog.lE_fieldname.text()

            # is duplicate
            is_duplicate = False
            if dialog.rb_cls.isChecked():
                is_duplicate = dialog.cb_duplicate.isChecked()

            classes = {}
            if dialog.rb_box.isChecked() or dialog.rb_cls.isChecked():
                for idx, line_edit in enumerate(dialog.cur_class_edit):
                    classes[idx] = line_edit.text()
            classes = json.dumps(classes)

            rowid = self.db_manager.create_label_field(
                name=field_name,
                dataset_id=self.cur_dataset_db_idx,
                label_format=label_format,
                label_type=label_type,
                is_duplicate=is_duplicate,
                detail=classes
            )
            self.logger.info(f"라벨 필드 데이터베이스 저장: {label_format}-{label_type} / label_field row: {rowid}")

            self.clear_ui_label_fields()
            self.draw_ui_label_fields()

            self.statusbar.showMessage(f"라벨 필드 추가 완료 - 라벨 포맷: {label_format} / 라벨 타입: {label_type}")
            self.logger.info(f"라벨 필드 추가 완료 - 라벨 포맷: {label_format} / 라벨 타입: {label_type}")

    def edit_label_field(self):
        self.logger.info("클릭 - 라벨 필드 수정")

        # label info process
        cap_field = [img_cap_field_name[0] for img_cap_field_name in self.label_field_image_caps]
        cls_field = {}
        for image_cls in self.label_field_image_cls:
            field_name = image_cls[0]
            field_cls_data = self.label_field_name_dict_classname_to_idx[field_name]
            cls_field[field_name] = field_cls_data

        label_field = {
            'boxes-box': self.label_field_name_dict_classname_to_idx.get('boxes-box'),
            'image-caption': cap_field,
            'image-cls': cls_field
        }

        dialog = EditLabelFieldDialog(self, label_info=label_field)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("라벨 필드 수정 취소")
            return
        elif ret == QDialog.DialogCode.Accepted:
            orig_label = dialog.orig_label_field
            cur_label = dialog.cur_label_field
            # boxes-box
            orig_bbox = orig_label['boxes-box']
            cur_bbox = cur_label['boxes-box']
            bbox_detail = {}
            for idx, (le, cls_name) in enumerate(cur_bbox.items()):
                # all: change detail
                bbox_detail[idx] = cls_name
                if le in orig_bbox.keys():
                    del orig_bbox[le]
            # Delete: label_data in DB
            label_field_idx = self.label_fields_dict_name_to_idx['boxes-box']
            for del_name in orig_bbox.values():
                cls_idx = self.label_field_name_dict_classname_to_idx['boxes-box'][del_name]
                self.db_manager.delete_label_data(cls=cls_idx, label_field_id=label_field_idx)

            # Update: label_field table in DB
            classes = json.dumps(bbox_detail)
            where = {'label_field_id': label_field_idx}
            if dialog.is_changed:
                self.db_manager.update_label_field(where, detail=classes)

            # image-cap
            orig_img_caps = orig_label['image-caption']
            cur_img_caps = cur_label['image-caption']
            for le, field_name in cur_img_caps.items():
                label_field_idx = self.label_fields_dict_name_to_idx[orig_img_caps[le]]
                if orig_img_caps[le] != field_name and dialog.is_changed:
                    where = {'label_field_id': label_field_idx}
                    self.db_manager.update_label_field(where, name=field_name)

            # image-cls
            orig_img_classes = orig_label['image-cls']
            cur_img_classes = cur_label['image-cls']
            for field_name, class_item in cur_img_classes.items():
                img_cls_detail = {}
                for idx, (le, class_name) in enumerate(class_item.items()):
                    # all: change detail
                    img_cls_detail[idx] = class_name
                    if le in orig_img_classes[field_name].keys():
                        del orig_img_classes[field_name][le]
                # Delete: label_data in DB
                img_cls_field_idx = self.label_fields_dict_name_to_idx[field_name]
                # Delete img-cls label-data
                for del_name in orig_img_classes[field_name].values():
                    cls_idx = self.label_field_name_dict_classname_to_idx[field_name][del_name]
                    self.db_manager.delete_label_data(label_field_id=img_cls_field_idx, cls=cls_idx)
                # Update
                classes = json.dumps(img_cls_detail)
                where = {'label_field_id': img_cls_field_idx}
                if dialog.is_changed:
                    self.db_manager.update_label_field(where, detail=classes)

            self.clear_ui_label_data()
            self.clear_ui_label_fields()
            self.draw_ui_label_fields()
            self.draw_ui_label_data()

            self.logger.info(f"라벨 필드 수정 완료")

    def delete_label_field(self):
        self.logger.info("클릭 - 라벨 필드 삭제")

        dialog = LabelsFieldDeleteDialog(self, label_info=self.label_fields_list_idx_name, db=self.db_manager)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            return
        elif ret == QDialog.DialogCode.Accepted:
            delete_field_name = []
            delete_idx = []
            for db_idx, label_item in dialog.field_dict.items():
                checkbox, label_field = label_item
                if checkbox.isChecked():
                    delete_field_name.append(label_field)
                    delete_idx.append(db_idx)

            # Remove in DB
            for idx in delete_idx:
                self.db_manager.delete_label_field_by_label_field_id(idx)

            text = f"'{delete_field_name.pop(0)}'"
            for label_field in delete_field_name:
                text += f", '{label_field}'"
            msgBox = QMessageBox()
            msgBox.setText(f"{len(delete_idx)}개의 필드 {text}을(를) 삭제하였습니다.")
            msgBox.exec()

            # Update UI
            self.clear_ui_label_fields()
            self.draw_ui_label_fields()

            self.statusbar.showMessage(f"{len(delete_idx)}개의 라벨 필드 삭제: {text}")
            self.logger.info(f"{len(delete_idx)}개의 라벨 필드 삭제: {text}")

    def create_bbox_shape(self, xyxy, class_name, pixmap_size):
        x1, y1, x2, y2 = rel_to_xyxy(xyxy, pixmap_size)
        box = Shape(label=class_name)
        box.add_point(QPointF(x1, y1))
        box.add_point(QPointF(x2, y1))
        box.add_point(QPointF(x2, y2))
        box.add_point(QPointF(x1, y2))
        g_color = generate_color_by_text(class_name)
        box.set_color(line_color=g_color, fill_color=g_color)
        self.cur_inner_tab.shapes.append(box)

        return self.cur_inner_tab.get_last_shape()

    def create_bbox_item(self, shape: Shape):
        item = BoxQListWidgetItem(shape.label)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)
        item.setBackground(generate_color_by_text(shape.label))
        self.bbox_items_to_shapes[item] = shape
        self.bbox_shapes_to_items[shape] = item
        self.bbox_listwidget.addItem(item)

    def select_upper_image(self):
        self.logger.info("클릭 - 상단 이미지")
        if not self.image_list_widget.selectedItems():
            self.image_list_widget.selectRow(0)
            self.draw_image_item(self.image_list_widget.item(0, 0))
        else:
            current_img_item_row_idx = self.image_list_widget.selectedIndexes()[0].row()
            if current_img_item_row_idx == 0:
                return
            self.check_autosave()

            current_img_item_row_idx = max(current_img_item_row_idx-1, 0)
            self.image_list_widget.selectRow(current_img_item_row_idx)
            self.draw_image_item(self.image_list_widget.item(current_img_item_row_idx, 0))

    def select_lower_image(self):
        self.logger.info("클릭 - 하단 이미지")
        if not self.image_list_widget.selectedItems():
            self.image_list_widget.selectRow(0)
            self.draw_image_item(self.image_list_widget.item(0, 0))
        else:
            num_row = self.image_list_widget.rowCount()
            current_img_item_row_idx = self.image_list_widget.selectedIndexes()[0].row()
            if current_img_item_row_idx == num_row - 1:
                return
            self.check_autosave()

            current_img_item_row_idx = min(current_img_item_row_idx + 1, num_row - 1)
            self.image_list_widget.selectRow(current_img_item_row_idx)
            self.draw_image_item(self.image_list_widget.item(current_img_item_row_idx, 0))

    def select_inner_tab_widget(self, index):
        # change variable
        self.cur_inner_tab = self.tab_widget.currentWidget()
        self.cur_inner_tab_ui_idx = index
        self.cur_inner_tab_name = self.tab_widget.tabText(index)
        self.cur_dataset_name = self.cur_inner_tab_name
        self.cur_dataset_db_idx = self.dataset_dict_name_to_idx[self.cur_dataset_name]

        # reset left image list
        self.clear_ui_image_list()
        self.draw_ui_image_list()

        # Reset pixmap, right labels(box list and shape, item)
        self.clear_ui_image()
        self.clear_ui_label_data()

        # Reset label fields
        self.clear_ui_label_fields()
        self.draw_ui_label_fields()

        self.logger.info(f"탭 변경 - index / name: {index} / {self.cur_inner_tab_name}")

    def is_valid_change_img_caption(self):
        if self.cur_image_db_idx == -1:
            for cap_data in self.label_field_image_caps:
                plain_text = cap_data[1]
                if len(plain_text.toPlainText()):
                    msgBox = QMessageBox(text="이미지 캡션 라벨은 이미지를 선택 후 입력할 수 있습니다.")
                    msgBox.exec()
                    self.clear_ui_img_label_captions()
        else:
            return

    def is_valid_change_img_cls(self):
        if self.cur_image_db_idx == -1:
            for cls_data in self.label_field_image_cls:
                group_box = cls_data[1]
                for c in group_box.children():
                    if type(c) in [QRadioButton, QCheckBox]:
                        if c.isChecked():
                            msgBox = QMessageBox(text="이미지 클래스 라벨은 이미지 선택 후 입력 가능합니다.")
                            msgBox.exec()
                            self.clear_ui_img_label_cls()
        else:
            return

    def set_create_mode(self):
        if self.label_field_boxes_box:
            self.cur_inner_tab.set_editing(False)
        else:
            msgBox = QMessageBox(text="박스형 라벨 필드가 존재하지 않습니다.")
            msgBox.exec()

    def set_edit_mode(self):
        self.cur_inner_tab.set_editing(True)

    def draw_new_bbox_label(self):
        classes = self.label_field_name_dict_classname_to_idx['boxes-box']
        basic_class_name = list(classes.keys())[0]
        g_color = generate_color_by_text(basic_class_name)
        shape = self.cur_inner_tab.set_last_label(basic_class_name, line_color=g_color, fill_color=g_color)
        shape.class_idx = 0
        self.create_bbox_item(shape)
        self.cur_inner_tab.set_editing(True)
        self.is_label_change = True

        item = self.bbox_shapes_to_items[shape]
        item.setSelected(True)

    def clear_selected_bbox_label(self):
        shape = self.cur_inner_tab.delete_selected_shape()
        if shape is None:
            return
        item = self.bbox_shapes_to_items[shape]
        self.bbox_listwidget.takeItem(self.bbox_listwidget.row(item))
        del self.bbox_shapes_to_items[shape]
        del self.bbox_items_to_shapes[item]

        self.is_label_change = True
        self.statusbar.showMessage(f"바운딩 박스 라벨 제거: {shape.label}")

    def save_db_labels(self):
        # Delete entire label in current image
        self.db_manager.delete_label_data(image_data_id=self.cur_image_db_idx)

        # Save image-cap label
        self.save_db_img_label_captions()

        # Save image-cls label
        self.save_img_label_cls()

        # Save boxes-box label
        self.save_bbox_labels()

        # 박스 - 캡션

        # 박스 - 클래스

    def save_db_img_label_captions(self):
        for cap_label in self.label_field_image_caps:
            field_name, plain_text = cap_label
            caption_text = plain_text.toPlainText()
            label_field_id = self.label_fields_dict_name_to_idx[field_name]

            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_db_idx,
                label_field_id=label_field_id,
                is_box=0,
                caption=caption_text
            )

            self.logger.info(f"이미지 캡션 라벨 저장 완료 - label_data_id: {lastrowid}")

    def save_img_label_cls(self):
        field_idx_class = []
        for cls_label in self.label_field_image_cls:
            field_name, group_box = cls_label
            for c in group_box.children():
                if type(c) in [QRadioButton, QCheckBox]:
                    if c.isChecked():
                        field_idx = self.label_fields_dict_name_to_idx[field_name]
                        label_cls = self.label_field_name_dict_classname_to_idx[field_name][c.text()]
                        field_idx_class.append([field_idx, label_cls])
                else:   # hlo
                    continue
        for cls_data in field_idx_class:
            label_field_id, cls = cls_data
            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_db_idx,
                label_field_id=label_field_id,
                is_box=0,
                cls=cls
            )

            self.logger.info(f"이미지 클래스 라벨 저장 완료 - label_data_id: {lastrowid}")

    def save_bbox_labels(self, only_new=False):
        if not self.label_field_boxes_box:
            return

        boxes = []
        label_field_idx, list_widget = self.label_field_boxes_box

        if only_new is True:
            shapes_to_items = self.bbox_new_shapes_to_items
        else:
            shapes_to_items = self.bbox_shapes_to_items

        for box_shape, list_widget_item in shapes_to_items.items():
            points = box_shape.points
            xyxy = get_xyxy(points)
            pixmap_size = self.cur_inner_tab.pixmap.size()
            rel_xyxy = xyxy_to_rel(xyxy, pixmap_size)
            cls = self.label_field_name_dict_classname_to_idx['boxes-box'][list_widget_item.text()]

            lastrowid = self.db_manager.create_label_data(
                image_data_id=self.cur_image_db_idx,
                label_field_id=label_field_idx,
                is_box=1,
                coord=str(list(rel_xyxy)),
                cls=cls
            )
            boxes.append(lastrowid)

        self.bbox_new_shapes_to_items = {}

        self.logger.info(f"바운딩 박스 라벨 저장 완료 - {len(boxes)}개 : {boxes}")

    def keyPressEvent(self, event):
        if Qt.Key.Key_Comma == event.key():
            self.select_upper_image()
        elif Qt.Key.Key_Period == event.key():
            self.select_lower_image()

        if self.cur_inner_tab.selected_shape is not None:
            shape = self.cur_inner_tab.selected_shape
            if self._is_change_box_class is False and event.key() == Qt.Key.Key_Alt:
                self._is_change_box_class = True
                self.is_label_change = True
                self.statusbar.showMessage("Enable to change class number")
                return
            if self._is_change_box_class is True and event.text().isdigit():
                press_num = event.text()
                self._change_box_class.append(press_num)
                _change_cls = "".join(self._change_box_class)
                if _change_cls in list(self.label_field_name_dict_classname_to_idx['boxes-box'].values()):
                    shape.class_idx = (int(_change_cls))
                    for cls_name, cls_idx in self.label_field_name_dict_classname_to_idx['boxes-box'].items():
                        if cls_idx == _change_cls:
                            g_color = generate_color_by_text(cls_name)
                            shape.label = cls_name
                            shape.line_color = g_color
                            shape.fill_color = g_color
                            break
                    item = self.bbox_shapes_to_items[shape]
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

    def change_autosave_checkbox(self, arg):
        if arg == Qt.CheckState.Checked.value:
            self.is_autosave = True
        else:
            self.is_autosave = False

    def check_autosave(self):
        if self.is_autosave is True and self.is_label_change is True:
            self.save_db_labels()

    def shape_selection_changed(self):
        if self._no_selection_slot:
            self._no_selection_slot = False
        else:
            shape = self.cur_inner_tab.selected_shape
            if shape:
                self.bbox_shapes_to_items[shape].setSelected(True)
            else:
                self.bbox_listwidget.clearSelection()

    def label_selection_changed(self):
        # get current item
        items = self.bbox_listwidget.selectedItems()
        item = items[0] if items else None
        if item and self.cur_inner_tab.is_editing():
            self._no_selection_slot = True
            shape = self.bbox_items_to_shapes[item]
            self.cur_inner_tab.select_shape(shape)

    def label_item_changed(self, item):
        shape = self.bbox_items_to_shapes[item]
        label = item.text()
        if label != shape.label:
            shape.label = item.text()
            shape.line_color = generate_color_by_text(shape.label)
            # self.set_dirty()
        else:  # User probably changed item visibility
            self.cur_inner_tab.set_shape_visible(shape, item.checkState() == Qt.CheckState.Checked)

    def create_box_label_by_detection_entire_images(self, remove_label=True):
        self.logger.info(f"클릭 - 전체 이미지 디텍션 라벨 생성 - 기존 라벨 제거: {remove_label}")
        item_cnt = self.image_list_widget.rowCount()
        dialog = DetectionLabelsCreateDialog(self, weight=self.cfg.det_model_path, img_num=item_cnt)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("디텍션 라벨 생성 취소")
            return
        elif ret == QDialog.DialogCode.Accepted:
            box_num = 0
            for row_idx in range(item_cnt):
                img_idx_item = self.image_list_widget.item(row_idx, 0)
                img_idx = int(img_idx_item.text())
                self.image_list_widget.selectRow(row_idx)
                self.draw_image_item(img_idx_item)
                n = self.create_box_label_by_detection_one_image(img_idx, remove_label=remove_label)
                box_num += n

            self.statusbar.showMessage(f"Bounding box for {item_cnt} images created successfully: {box_num}")
            self.logger.info(f"Bounding box for {item_cnt} images created successfully: {box_num}")

    def create_box_label_by_detection_selected_images(self, remove_label=True):
        self.logger.info(f"클릭 - 선택 이미지 디텍션 라벨 생성 - 기존 라벨 제거: {remove_label}")
        if self.image_list_widget.check_selected_row_num() == 0:
            self.statusbar.showMessage("1장 이상의 이미지를 선택해주세요.")
            msgBox = QMessageBox(text="이미지를 선택해주세요.")
            msgBox.setWindowTitle("이미지 미선택 오류")
            msgBox.exec()
            return

        imgs_idx = dict()
        for item in self.image_list_widget.selectedItems():
            if int(self.image_list_widget.item(item.row(), 0).text()) not in imgs_idx:
                imgs_idx[int(self.image_list_widget.item(item.row(), 0).text())] = item
        dialog = DetectionLabelsCreateDialog(self, weight=self.cfg.det_model_path, img_num=len(imgs_idx))
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("디텍션 라벨 생성 취소")
            return
        elif ret == QDialog.DialogCode.Accepted:
            box_num = 0
            for img_idx, item in imgs_idx.items():
                self.image_list_widget.selectRow(item.row())
                self.draw_image_item(item)
                n = self.create_box_label_by_detection_one_image(img_idx, remove_label=remove_label)
                box_num += n

            self.statusbar.showMessage(f"Bounding box for {len(imgs_idx)} images created successfully: {box_num}")
            self.logger.info(f"Bounding box for {len(imgs_idx)} images created successfully: {box_num}")

    def create_box_label_by_detection_current_image(self, remove_label=True):
        self.logger.info(f"클릭 - 현재 이미지 디텍션 라벨 생성 - 기존 라벨 제거: {remove_label}")
        if self.image_list_widget.check_selected_row_num() == 0:
            self.statusbar.showMessage("이미지를 선택해주세요.")
            msgBox = QMessageBox(text="이미지를 선택해주세요.")
            msgBox.setWindowTitle("이미지 미선택 오류")
            msgBox.exec()
            return
        elif self.image_list_widget.check_selected_row_num() > 1:
            self.statusbar.showMessage("이미지를 1장만 선택해주세요.")
            msgBox = QMessageBox(text="이미지를 1장만 선택해주세요.")
            msgBox.setWindowTitle("다중 이미지 선택 오류")
            msgBox.exec()
            return

        dialog = DetectionLabelsCreateDialog(self, weight=self.cfg.det_model_path, img_num=1)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            self.logger.info("디텍션 라벨 생성 취소")
            return
        elif ret == QDialog.DialogCode.Accepted:
            box_num = self.create_box_label_by_detection_one_image(self.cur_image_db_idx, remove_label=remove_label)

            self.statusbar.showMessage(f"Bounding box created successfully: {box_num}")
            self.logger.info(f"Bounding box for current image created successfully: {box_num}")

    def create_box_label_by_detection_one_image(self, image_idx, remove_label=True):
        # Check boxes-box label is exist.
        if 'boxes-box' not in self.label_field_name_dict_classname_to_idx:
            msgBox = QMessageBox(text="박스형-박스 라벨 필드가 존재하지 않습니다.")
            msgBox.exec()
            self.logger.warning("박스 형 - 박스 라벨 필드 없이 추론 시도")
            return

        # Delete Current image box label
        if remove_label is True:
            self.db_manager.delete_label_data(image_data_id=image_idx, is_box=1)
            self.clear_ui_bbox_label_data()

        if self.detector is None:
            self.detector = ObjectDetector(cfg=self.cfg)
        image_fid = self.image_list_widget.fid_dict[image_idx]
        img = self.weed_manager.get_image(fid=image_fid, pil=False)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        det = self.detector.run_np(img)
        img_h, img_w = img.shape[:2]
        cls_idx_to_name = {int(v): k for k, v in self.label_field_name_dict_classname_to_idx['boxes-box'].items()}
        ret_num = 0
        for d in det:
            abs_xyxy = d[:4]
            rel_xyxy = absxyxy_to_relxyxy(abs_xyxy, img_w, img_h)
            cls = int(d[5])
            cls = self.cfg.det_infer_cls.get(cls) if self.cfg.det_infer_cls is not None and self.cfg.det_infer_cls.get(cls) else cls
            if cls not in cls_idx_to_name.keys():
                continue
            ret_num += 1
            cls_name = cls_idx_to_name[cls]

            # Shape and Item
            shape = self.create_bbox_shape(rel_xyxy, cls_name, self.cur_inner_tab.pixmap.size())
            self.create_bbox_item(shape)
            if remove_label is False:
                item = self.bbox_shapes_to_items[shape]
                self.bbox_new_shapes_to_items[shape] = item

        # Save label in DB
        self.save_bbox_labels(only_new=not remove_label)

        return ret_num

    def export_yolo_detection_dataset(self):
        dialog = ExportDialog(self)
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Rejected:
            return

        path = dialog.dirname
        train, val, test = dialog.train_ratio, dialog.val_ratio, dialog.test_ratio
        is_shuffle = dialog.is_shuffle
        self.logger.info(f"YOLO 감지 데이터 셋 내보내기 시작 : {self.cur_inner_tab_name}")
        st = time.time()
        imgs_idx = set()
        label_field_id = self.label_fields_dict_name_to_idx['boxes-box']
        # All images
        if len(self.image_list_widget.selectedItems()) == 0:
            for idx in range(self.image_list_widget.rowCount()):
                imgs_idx.add(int(self.image_list_widget.item(idx, 0).text()))
        # Selected images
        else:
            for item in self.image_list_widget.selectedItems():
                imgs_idx.add(int(self.image_list_widget.item(item.row(), 0).text()))

        # check shuffle is needed
        imgs_idx = list(imgs_idx)
        if is_shuffle is True:
            random.shuffle(imgs_idx)
        if is_shuffle is False:
            imgs_idx = sorted(imgs_idx)
        train_num = int(len(imgs_idx) * train)
        val_num = int(len(imgs_idx) * (train + val))
        test_num = int(len(imgs_idx) * (train + val + test))

        # Set save path
        dirname = path
        dataset_name = self.cur_inner_tab_name + f"_{datetime.now().strftime('%y%m%d_%H%M%S')}"
        dataset_path = os.path.join(dirname, dataset_name)
        os.makedirs(dataset_path, exist_ok=True)

        # save meta yaml
        label_field_info = self.db_manager.read_label_field_by_dataset_id(self.cur_dataset_db_idx)
        boxes_box_field = None
        for label_field in label_field_info:
            if label_field[3] == 0 and label_field[4] == 0:
                boxes_box_field = eval(label_field[6])
                break
        meta_data = {}
        if boxes_box_field:
            meta_data['names'] = [cls_name for cls_name in boxes_box_field.values()]
            meta_data['nc'] = len(boxes_box_field)
        meta_data['path'] = dataset_path
        if train != 0.:
            meta_data['train'] = './train/images'
        if val != 0.:
            meta_data['val'] = './val/images'
        if test != 0.:
            meta_data['test'] = './test/images'
        with open(os.path.join(str(dataset_path), 'data.yaml'), 'w', encoding='utf8') as f:
            yaml.dump(meta_data, f, allow_unicode=True, sort_keys=False)
        # result txt
        result_file = open(os.path.join(str(dataset_path), 'result.txt'), 'w', encoding='utf8')
        result_file.write(f"Dataset: {self.cur_dataset_name}\n")
        t = str([f"{int(v)}: {k}" for k, v in self.label_field_name_dict_classname_to_idx['boxes-box'].items()])
        class_num = len(self.label_field_name_dict_classname_to_idx['boxes-box'])
        result_file.write(f"Total image num: {len(imgs_idx)}\n")
        result_file.write(f"Classes: {t}\n")
        result_file.write("-"*20+'\n')

        # Save Train set
        if train != 0.:
            # make train, images, labels dirs
            train_dir = os.path.join(str(dataset_path), "train")
            t_img_dir, t_lb_dir = os.path.join(train_dir, "images"), os.path.join(train_dir, "labels")
            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(t_img_dir, exist_ok=True)
            os.makedirs(t_lb_dir, exist_ok=True)
            result_file.write(f"Train image num: {len(imgs_idx[:train_num])}\n")
            class_data = {i: 0 for i in range(class_num)}
            for i in imgs_idx[:train_num]:
                img_info = self.db_manager.read_image_data_by_image_data_id(i)[0]
                img_file = f"{i:06d}_{img_info[2]}"
                img_path = os.path.join(t_img_dir, img_file)

                # save img
                image_fid = self.image_list_widget.fid_dict[i]
                img = self.weed_manager.get_image(fid=image_fid)
                img.save(img_path, compress_level=0)

                # save label
                label_info = self.db_manager.read_label_data(image_data_id=i, label_field_id=label_field_id)
                if label_info:
                    label_path = os.path.join(t_lb_dir, os.path.splitext(img_file)[0] + '.txt')
                    with open(label_path, 'w', encoding='utf8') as f:
                        for l_info in label_info:
                            box_coord = eval(l_info[5])
                            box_class = l_info[6]
                            box_xywh = (f"{(box_coord[2] + box_coord[0])/2:.6f} "
                                        f"{(box_coord[3] + box_coord[1])/2:.6f} "
                                        f"{box_coord[2] - box_coord[0]:.6f} {box_coord[3] - box_coord[1]:.6f}")
                            label_str = f"{box_class} {box_xywh}\n"
                            f.write(label_str)
                            class_data[int(box_class)] += 1
            t = str([f"{int(k)}: {v}" for k, v in class_data.items()])
            result_file.write(f"labels: {t}\n")
            result_file.write("-" * 20 + '\n')

        # Save Val set
        if val != 0.:
            val_dir = os.path.join(str(dataset_path), "val")
            v_img_dir, v_lb_dir = os.path.join(val_dir, "images"), os.path.join(val_dir, "labels")
            os.makedirs(val_dir, exist_ok=True)
            os.makedirs(v_img_dir, exist_ok=True)
            os.makedirs(v_lb_dir, exist_ok=True)
            result_file.write(f"Val image num: {len(imgs_idx[train_num:val_num])}\n")
            class_data = {i: 0 for i in range(class_num)}
            for i in imgs_idx[train_num:val_num]:
                img_info = self.db_manager.read_image_data_by_image_data_id(i)[0]
                img_file = f"{i:06d}_{img_info[2]}"
                img_path = os.path.join(v_img_dir, img_file)

                # save img
                image_fid = self.image_list_widget.fid_dict[i]
                img = self.weed_manager.get_image(fid=image_fid)
                img.save(img_path, compress_level=0)

                # save label
                label_info = self.db_manager.read_label_data(image_data_id=i, label_field_id=label_field_id)
                if label_info:
                    label_path = os.path.join(v_lb_dir, os.path.splitext(img_file)[0] + '.txt')
                    with open(label_path, 'w', encoding='utf8') as f:
                        for l_info in label_info:
                            box_coord = eval(l_info[5])
                            box_class = l_info[6]
                            box_xywh = (f"{(box_coord[2] + box_coord[0])/2:.6f} "
                                        f"{(box_coord[3] + box_coord[1])/2:.6f} "
                                        f"{box_coord[2] - box_coord[0]:.6f} {box_coord[3] - box_coord[1]:.6f}")
                            label_str = f"{box_class} {box_xywh}\n"
                            f.write(label_str)
                            class_data[int(box_class)] += 1
            t = str([f"{int(k)}: {v}" for k, v in class_data.items()])
            result_file.write(f"labels: {t}\n")
            result_file.write("-" * 20 + '\n')

        # Save Test set
        if test != 0.:
            test_dir = os.path.join(str(dataset_path), "test")
            te_img_dir, te_lb_dir = os.path.join(test_dir, "images"), os.path.join(test_dir, "labels")
            os.makedirs(test_dir, exist_ok=True)
            os.makedirs(te_img_dir, exist_ok=True)
            os.makedirs(te_lb_dir, exist_ok=True)
            result_file.write(f"Test image num: {len(imgs_idx[:train_num])}\n")
            class_data = {i: 0 for i in range(class_num)}
            for i in imgs_idx[val_num:]:
                img_info = self.db_manager.read_image_data_by_image_data_id(i)[0]
                img_file = f"{i:06d}_{img_info[2]}"
                img_path = os.path.join(te_img_dir, img_file)

                # save img
                image_fid = self.image_list_widget.fid_dict[i]
                img = self.weed_manager.get_image(fid=image_fid)
                img.save(img_path, compress_level=0)

                # save label
                label_info = self.db_manager.read_label_data(image_data_id=i, label_field_id=label_field_id)
                if label_info:
                    label_path = os.path.join(te_lb_dir, os.path.splitext(img_file)[0] + '.txt')
                    with open(label_path, 'w', encoding='utf8') as f:
                        for l_info in label_info:
                            box_coord = eval(l_info[5])
                            box_class = l_info[6]
                            box_xywh = (f"{(box_coord[2] + box_coord[0])/2:.6f} "
                                        f"{(box_coord[3] + box_coord[1])/2:.6f} "
                                        f"{box_coord[2] - box_coord[0]:.6f} {box_coord[3] - box_coord[1]:.6f}")
                            label_str = f"{box_class} {box_xywh}\n"
                            f.write(label_str)
                            class_data[int(box_class)] += 1
            t = str([f"{int(k)}: {v}" for k, v in class_data.items()])
            result_file.write(f"labels: {t}\n")
            result_file.write("-" * 20 + '\n')

        result_file.close()
        self.logger.info(f"YOLO 감지 데이터 셋 내보내기 완료: {self.cur_inner_tab_name} / 소요: {time.time()-st:.3f} sec")


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
