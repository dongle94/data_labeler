# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.db_manager = None

        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)

    def create_dataset(self):
        ds_create = DSCreate(self.db_manager, self)
        ds_create.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ...

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
