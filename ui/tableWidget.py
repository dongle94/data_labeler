from PySide6.QtWidgets import QTabWidget


class ImagesTableWidget(QTabWidget):
    def __init__(self, parent=None):
        super(ImagesTableWidget, self).__init__(parent)