import sys
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal

from utils.logger import get_logger
from ui.ui_dataset import Ui_DS_Create
from ui.ui_basic_dialog import Ui_DS_Delete
from utils.checks import is_empty


class DSCreate(QDialog, Ui_DS_Create):
    create_dataset = Signal(str, str)

    def __init__(self, parent=None, db=None):
        super(DSCreate, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.db_manager = db
        self.logger = get_logger()

        # Signal & Slot
        self.pB_ds_create.clicked.connect(self.create_ds)
        self.pB_ds_cancel.clicked.connect(self.cancel)
        self.create_dataset.connect(self.parent().draw_dataset)

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

        self.create_dataset.emit(ds_name, ds_type)

        self.logger.info(f"데이터 셋 생성: {ds_name}-{ds_type}-{ds_desc}")

    def cancel(self):
        self.close()

    def get_ds_type(self):
        if self.rB_dstype_image.isChecked():
            return 0
        elif self.rB_dstype_Statistics.isChecked():
            return 1


class DSDelete(QDialog, Ui_DS_Delete):
    def __init__(self, parent=None, ds_name="", db=None):
        super(DSDelete, self).__init__(parent)
        self.setupUi(self)

        self.ds_name = ds_name
        self.db_manager = db
        self.logger = get_logger()

        self.label.setText(f"{ds_name} 데이터 셋을 삭제하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonBox.accepted.connect(self.delete_ds)
        self.buttonBox.rejected.connect(self.cancel)

    def delete_ds(self):
        # remove dataset in tabwidget
        self.parent().tW_img.removeTab(self.parent().tW_img.currentIndex())

        # delete dataset in database
        try:
            self.db_manager.delete_dataset(self.ds_name)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText(f"데이터 셋 삭제에 실패했습니다: {e}")
            msgBox.exec()
            return

        self.logger.info(f"데이터 셋 삭제: {self.ds_name}")

    def cancel(self):
        self.close()
