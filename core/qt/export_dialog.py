from PySide6.QtWidgets import QDialog

from ui.ui_export_dialog import Ui_Dialog


class ExportDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
