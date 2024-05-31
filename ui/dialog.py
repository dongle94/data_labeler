import sys
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal

from utils.logger import get_logger
from ui.ui_dataset import Ui_DS_Create
from ui.ui_basic_dialog import Ui_Basic_Dialog
from ui.widget import ImageTabInnerWidget
from utils.checks import is_empty


class DSCreate(QDialog, Ui_DS_Create):
    def __init__(self, parent=None, db=None):
        super(DSCreate, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.db_manager = db
        self.logger = get_logger()

        # Signal & Slot
        self.pB_ds_create.clicked.connect(self.create_ds)
        self.pB_ds_cancel.clicked.connect(self.cancel)

    def create_ds(self):
        ds_name = self.lE_dataset_name.text()
        ds_type = self.get_ds_type()
        ds_desc = self.pTE_ds_desc.toPlainText()

        # check valid format
        if is_empty(ds_name) is True:
            msgBox = QMessageBox()
            msgBox.setText("데이터 셋 이름은 공백이 될 수 없습니다.")
            msgBox.exec()
            return

        # db search with ds_name
        res = self.db_manager.read_dataset_detail(ds_name)
        if len(res) != 0:
            msgBox = QMessageBox()
            msgBox.setText("이미 존재하는 데이터 셋 이름입니다.")
            msgBox.exec()
            return

        # db insert
        try:
            self.db_manager.create_dataset(ds_name, ds_type, ds_desc)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText(f"데이터 셋 생성에 실패했습니다: {e}")
            msgBox.exec()
            return

        msgBox = QMessageBox()
        msgBox.setText(f"데이터 셋 생성에 성공하였습니다.")
        msgBox.exec()
        self.accept()

        # (GUI)Draw dataset in tabWidget
        wg = ImageTabInnerWidget(self)
        self.parent().tW_img.addTab(wg, ds_name)

        # TODO add dataset desc

        self.logger.info(f"데이터 셋 생성: {ds_name}-{ds_type}-{ds_desc}")

    def cancel(self):
        self.close()
        self.logger.info("데이터 셋 생성 취소")

    def get_ds_type(self):
        if self.rB_dstype_image.isChecked():
            return 0
        elif self.rB_dstype_Statistics.isChecked():
            return 1


class DSDelete(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, ds_name="", weed=None, db=None):
        super(DSDelete, self).__init__(parent)
        self.setupUi(self)

        self.ds_name = ds_name
        self.weed_manager = weed
        self.db_manager = db
        self.logger = get_logger()

        self.label.setText(f"{ds_name} 데이터 셋을 삭제하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonBox.accepted.connect(self.delete_ds)
        self.buttonBox.rejected.connect(self.cancel)

    def delete_ds(self):
        tab_widget = self.parent().tW_images
        # Get All image url in that inner tab
        img_num = len(tab_widget.url_dict)

        # Delete All images in weedfs
        for db_idx, img_url in tab_widget.url_dict.items():
            self.weed_manager.delete_file(url=img_url)

        # delete dataset in database
        try:
            self.db_manager.delete_dataset(self.ds_name)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText(f"데이터 셋 삭제에 실패했습니다: {e}")
            msgBox.exec()
            return

        self.logger.info(f"데이터 셋 삭제: {self.ds_name} / 지워진 이미지 수: {img_num}")
        self.parent().tW_img.removeTab(self.parent().tW_img.currentIndex())

    def cancel(self):
        self.close()
        self.logger.info("데이터 셋 삭제 취소")


class ImageDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, image_num=0, weed=None, db=None):
        super(ImageDeleteDialog, self).__init__(parent)
        self.setupUi(self)

        self.weed_manager = weed
        self.db_manager = db
        self.logger = get_logger()

        self.label.setText(f"{image_num} 개의 이미지를 삭제 하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonBox.accepted.connect(self.delete_images)
        self.buttonBox.rejected.connect(self.cancel)

    def delete_images(self):
        # Get DB Index
        db_idx = set()
        image_list_table_widget = self.parent().tW_images
        for item in image_list_table_widget.selectedItems():
            img_db_idx = image_list_table_widget.item(item.row(), 0).text()
            db_idx.add(img_db_idx)

        # Get Weedfs url
        for img_db_idx in db_idx:
            weedfs_url = image_list_table_widget.url_dict[int(img_db_idx)]

            # Delete Weedfs image
            ret = self.weed_manager.delete_file(url=weedfs_url)

            # Delete in DB Table
            if ret is True:
                self.db_manager.delete_image_by_image_id(img_db_idx)

        # Draw again
        self.parent().draw_image_list_widget()


    def cancel(self):
        self.close()
        self.logger.info("이미지 삭제 취소")
