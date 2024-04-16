# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QLabel
from ui.ui_mainwindow import Ui_MainWindow




if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ...
    label = QLabel('HELLO PYSIDE')
    label.show()
    sys.exit(app.exec())
