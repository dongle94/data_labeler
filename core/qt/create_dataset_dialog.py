from PySide6.QtWidgets import QDialog

from ui.ui_create_dataset_dialog import Ui_Dialog


class CreateDatasetDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(CreateDatasetDialog, self).__init__(parent)
        self.setupUi(self)

        # Signal & Slot

    def get_dataset_type(self):
        if self.rB_dstype_image.isChecked():
            return 0
        elif self.rB_dstype_Statistics.isChecked():
            return 1
