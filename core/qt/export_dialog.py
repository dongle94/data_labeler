from PySide6.QtWidgets import QDialog, QDialogButtonBox

from utils.logger import get_logger
from ui.ui_export_dialog import Ui_Dialog
from utils.qt import get_dir_dialog
from utils.checks import is_empty


class ExportDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        self.logger = get_logger()

        self.dirname = ""
        self.train_ratio = 0.
        self.val_ratio = 0.
        self.test_ratio = 0.
        self.is_shuffle = False

        # Signal & Slot
        self.toolButton.clicked.connect(self.get_path)
        self.le_train.textChanged.connect(self.is_valid)
        self.le_val.textChanged.connect(self.is_valid)
        self.le_test.textChanged.connect(self.is_valid)

        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.export)

    def get_path(self):
        dir_dialog = get_dir_dialog(self)

        dirname = dir_dialog.getExistingDirectory(
            parent=self,
            caption='Select Directory',
            dir=""
        )
        if not dirname:
            self.logger.info("내보내기 경로 선택 취소")
            return
        self.dirname = dirname
        self.lineEdit.setText(dirname)
        self.is_valid()

    def export(self):
        self.train_ratio = float(self.le_train.text())
        self.val_ratio = float(self.le_val.text())
        self.test_ratio = float(self.le_test.text())
        self.is_shuffle = self.checkBox.isChecked()

    def cancel(self):
        self.close()
        self.logger.info("내보내기 취소")

    def is_valid(self):
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        if self.dirname and not is_empty(self.le_train.text()) and not is_empty(self.le_val.text()) \
                and not is_empty(self.le_test.text()):
            rtrain, rval, rtest = float(self.le_train.text()), float(self.le_val.text()), float(self.le_test.text())
            if int(rtrain * 1000) + int(rval * 1000) + int(rtest * 1000) == 1000:
                self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
