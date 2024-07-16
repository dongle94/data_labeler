from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget
from PySide6.QtGui import Qt


class ImagesTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(ImagesTableWidget, self).__init__(parent)

        # Data
        self.url_dict = {}
        self.fid_dict = {}

        # Ui
        self.verticalHeader().setVisible(False)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['ID', 'FileName'])

    def resizeEvent(self, event):
        tW_width = self.width()
        tW_height = self.height()
        self.setColumnWidth(0, int(tW_width * 0.195))
        self.setColumnWidth(1, int(tW_width * 0.795))

    def clear_image_list(self):
        self.clear()
        self.setRowCount(0)

        self.fid_dict = {}
        self.url_dict = {}

    def draw_image_list(self, images):
        self.setRowCount(len(images))

        for i, image in enumerate(images):
            img_idx = image[0]
            img_name = image[2]
            self.setItem(i, 0, QTableWidgetItem(str(img_idx)))
            self.setItem(i, 1, QTableWidgetItem(img_name))
            self.fid_dict[img_idx] = image[3]
            self.url_dict[img_idx] = image[4]

    def add_image_list(self, idx, name, fid, url):
        len_item = len(self.url_dict)
        self.insertRow(len_item)
        self.setItem(len_item, 0, QTableWidgetItem(str(idx)))
        self.setItem(len_item, 1, QTableWidgetItem(name))

        self.fid_dict[idx] = fid
        self.url_dict[idx] = url

    def keyPressEvent(self, event):
        if Qt.Key.Key_Up == event.key():
            self.window().select_upper_image()
        elif Qt.Key.Key_Down == event.key():
            self.window().select_lower_image()


class ImageTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(ImageTabWidget, self).__init__(parent)

