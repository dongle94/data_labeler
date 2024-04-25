import sys
from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtCore import Qt
from ui.ui_dataset import Ui_DS_Create


class DSCreate(QDialog, Ui_DS_Create):
    def __init__(self, parent=None):
        super(DSCreate, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Signal & Slot
        self.pB_ds_create.clicked.connect(self.create_ds)
        self.pB_ds_cancel.clicked.connect(self.cancel)

    def create_ds(self):
        ds_name = self.lE_dataset_name.text()
        ds_type = 0 if self.rB_dstype_image.isChecked() else 1
        ds_desc = self.pTE_ds_desc.toPlainText()
        print(ds_name, ds_type, ds_desc)
        # TODO check valid format
        # 이름 공백 x

        # TODO try db insert
        # 결과 반환

        # TODO finish each result
        # db pk 중복
        # 성공

        # self.close()

    def cancel(self):
        self.close()
