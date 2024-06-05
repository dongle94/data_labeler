# This Python file uses the following encoding: utf-8
import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QPlainTextEdit, \
    QGroupBox, QCheckBox, QRadioButton, QHBoxLayout
from PySide6.QtCore import Qt

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from utils.qt import create_label, create_button_group
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate, DSDelete, ImageDeleteDialog, AddLabelDialog
from ui.widget import ImageTabInnerWidget
from core.database import DBManager
from core.weedfs import SeaWeedFS


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
        self.cur_tab_idx = -1
        self.cur_dataset_idx = -1
        self.cur_tab_name = None

        # init drawing
        self.draw_dataset()
        self.draw_image_list_widget()
        self.clean_label_field()
        self.draw_label_field()

        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)

        self.tB_header_uploadImage.clicked.connect(self.insert_images)
        self.actionUpload_Image.triggered.connect(self.insert_images)
        self.tB_header_delDataset.clicked.connect(self.delete_dataset)
        self.actionDelete_Dataset.triggered.connect(self.delete_dataset)

        self.tB_header_delSelectedImage.clicked.connect(self.delete_images)
        self.actionDelete_Selected_Image.triggered.connect(self.delete_images)

        self.tW_img.currentChanged.connect(self.change_tab)

        self.tB_img_up.clicked.connect(self.get_upper_image)
        self.tB_img_down.clicked.connect(self.get_lower_image)
        self.tB_img_del.clicked.connect(self.delete_images)

        self.tW_images.itemClicked.connect(self.draw_image)

        self.pB_label_add.clicked.connect(self.add_label)

        self.logger.info("Success initializing MainWindow")

    def create_dataset(self):
        self.logger.info("Click 'dataset create'")
        ds_create = DSCreate(self, self.db_manager)
        ds_create.show()

    def delete_dataset(self):
        self.logger.info("Click 'dataset delete'")
        cur_idx = self.tW_img.currentIndex()
        cur_tab_name = self.tW_img.tabText(cur_idx)

        q_delete = DSDelete(self,
                            ds_name=cur_tab_name,
                            weed=self.weed_manager,
                            db=self.db_manager)
        q_delete.exec()

    def insert_images(self):
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
            # get current tab dataset_id
            ret = self.db_manager.read_dataset_detail(self.cur_tab_name)[0]
            dataset_id = ret[0]

            for f_idx, filename in enumerate(filenames):
                self.statusbar.showMessage(f"Upload image ... ({f_idx+1}/{len(filenames)})")

                ret = self.weed_manager.put_image_collection(image=filename, filename=filename)

                idx = self.db_manager.insert_image(
                    dataset_id=dataset_id,
                    filename=ret['filename'],
                    image_url=ret['url'],
                    width=ret['width'],
                    height=ret['height']
                )
                self.tW_images.add_image_list(idx, ret['filename'], ret['url'])
            self.logger.info("이미지 업로드 완료")
            self.statusbar.showMessage(f"Image upload Success")

    def delete_images(self):
        self.logger.info("Click 'Delete Image'")

        if len(self.tW_images.selectedItems()):
            self.statusbar.showMessage(f"{len(self.tW_images.selectedItems())} 개의 이미지 삭제 요청")
            q_delete = ImageDeleteDialog(self,
                                         image_num=len(self.tW_images.selectedItems()),
                                         weed=self.weed_manager,
                                         db=self.db_manager)
            q_delete.exec()
        else:
            self.statusbar.showMessage("이미지를 삭제하려면 1개 이상의 이미지를 선택해야합니다.")

    def add_label(self):
        self.logger.info("Click 'add_label'")

        add_label_dialog = AddLabelDialog(self, dataset_id=self.cur_dataset_idx, db=self.db_manager)
        add_label_dialog.show()

    def draw_dataset(self):
        ds = self.db_manager.read_dataset()

        for d in ds:
            ds_name = d[1]
            wg = ImageTabInnerWidget(self)
            self.tW_img.addTab(wg, ds_name)

        self.cur_tab_idx = self.tW_img.currentIndex()
        self.cur_tab_name = self.tW_img.tabText(self.cur_tab_idx)
        self.logger.info(f"Success drawing datasets - Current tab index, name: {self.cur_tab_idx}-{self.cur_tab_name}")

    def draw_image_list_widget(self):
        # get current tab dataset_id
        ret = self.db_manager.read_dataset_detail(self.cur_tab_name)[0]
        dataset_id = ret[0]
        self.cur_dataset_idx = dataset_id

        images = self.db_manager.read_image_by_dataset_id(dataset_id)
        self.tW_images.draw_image_list(images)

        self.logger.info(f"Success drawing image_list - Current tab index, dataset_id, image_len: "
                         f"{self.cur_tab_idx}-{dataset_id}, {len(images)} images")

    def draw_image(self, item: QTableWidgetItem):
        img_idx = self.tW_images.item(item.row(), 0).text()
        image_url = self.tW_images.url_dict[int(img_idx)]

        img = self.weed_manager.get_image(url=image_url)

        cur_tab = self.tW_img.currentWidget()
        cur_tab.set_qpixmap(img.toqpixmap(), scale=False)

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
        rets = self.db_manager.read_label_field_by_dataset_id(self.cur_dataset_idx)
        image_cap, image_cls = [], []
        boxes_box, boxes_cap, boxes_cls = [], [], []

        for ret in rets:
            field_name = ret[1]
            # dataset_id = ret[2]
            data_format = ret[3]
            data_type = ret[4]
            is_duplicate = ret[5]
            classes = json.loads(ret[6])

            if data_format == 0 and data_type == 0:     # boxes-box
                boxes_box.append(classes)
            elif data_format == 0 and data_type == 1:   # boxes-cap
                boxes_cap.append(field_name)
            elif data_format == 0 and data_type == 2:   # boxes-cls
                boxes_cls.append([field_name, is_duplicate, classes])
            elif data_format == 1 and data_type == 1:   # image-cap
                image_cap.append(field_name)
            elif data_format == 1 and data_type == 2:   # image-cls
                image_cls.append([field_name, is_duplicate, classes])

        # image-cap
        for f_name in image_cap:
            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            q_ptext = QPlainTextEdit(self)
            q_ptext.setMaximumHeight(int(self.height() * 0.07))
            self.vlo_img_label_field.addWidget(q_ptext)

        # image-cls
        for data in image_cls:
            f_name, is_duplicate, classes = data

            q_label = create_label(self,
                                   text=f_name,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="font-weight: bold")
            self.vlo_img_label_field.addWidget(q_label)
            group_box = create_button_group(self, horizontal=True, names=classes.values(), duplication=is_duplicate)
            self.vlo_img_label_field.addWidget(group_box)

        # boxes-box
        for classes in boxes_box:
            text = ""
            for idx, cls_name in classes.items():
                text += f"{idx}: {cls_name} "
            q_label = create_label(self,
                                   text=text,
                                   alignment=Qt.AlignmentFlag.AlignTop,
                                   stylesheet="color: blue; font-weight: bold;")
            self.vlo_box_label_field.addWidget(q_label)

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

    def change_tab(self, index):
        self.cur_tab_idx = index
        self.cur_tab_name = self.tW_img.tabText(index)

        self.draw_image_list_widget()

        self.logger.info(f"Success changing tab index, name: {index}-{self.cur_tab_name}")

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
