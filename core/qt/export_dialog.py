from PySide6.QtWidgets import QDialog, QDialogButtonBox

from utils.logger import get_logger
from ui.ui_export_dialog import Ui_Dialog
from utils.qt import get_dir_dialog


class ExportDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.logger = get_logger()

        self.dirname = ""

        # Signal & Slot
        self.toolButton.clicked.connect(self.get_path)

        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.export)

    def get_path(self):
        dirname = get_dir_dialog(self)
        self.dirname = dirname
        self.lineEdit.setText(dirname)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(bool(dirname))

    def export(self):
        self.parent().export_yolo_detection_dataset(self.dirname)

    def cancel(self):
        self.close()
        self.logger.info("내보내기 취소")
