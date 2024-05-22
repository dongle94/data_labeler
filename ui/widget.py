from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPainter, QPaintEvent, QPolygon, QPen, QColor, QBrush, Qt, QPixmap, QImage

from ui.label import ImgLabel, BoxOverlayLabel


class ImageTabInnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.bg_label = ImgLabel()

        layout = QVBoxLayout()
        self.img_labels = []
        layout.addWidget(self.bg_label)

        self.setLayout(layout)

    def set_image(self, img, scale=False):
        self.bg_label.setPixmap(QPixmap().fromImage(img))
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_label.setScaledContents(scale)

    def set_array(self, arr, scale=False):
        img = QImage(arr.data, arr.shape[1], arr.shape[0], QImage.Format.Format_BGR888)
        self.set_image(img, scale=scale)

    def set_file(self, path, scale=False):
        qpixmap = QPixmap().load(path)
        self.bg_label.setPixmap(qpixmap)
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_label.setScaledContents(scale)

    def set_qpixmap(self, pixmap: QPixmap, scale=False):
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_label.setScaledContents(scale)

    def add_box(self):
        self.img_labels.append(BoxOverlayLabel())
        # TODO add box


class ImagesTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(ImagesTableWidget, self).__init__(parent)

        # Data
        self.url_dict = {}

        # Ui
        self.verticalHeader().setVisible(False)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['ID', 'FileName'])

    def resizeEvent(self, event):
        tW_width = self.width()
        tW_height = self.height()
        self.setColumnWidth(0, int(tW_width * 0.195))
        self.setColumnWidth(1, int(tW_width * 0.795))

    def draw_image_list(self, images):
        self.setRowCount(len(images))

        self.url_dict = {}
        for i, image in enumerate(images):
            img_idx = image[0]
            img_name = image[2]
            self.setItem(i, 0, QTableWidgetItem(str(img_idx)))
            self.setItem(i, 1, QTableWidgetItem(img_name))
            self.url_dict[img_idx] = image[3]

    def add_image_list(self, idx, name, url):
        len_item = len(self.url_dict)
        self.insertRow(len_item)
        self.setItem(len_item, 0, QTableWidgetItem(str(idx)))
        self.setItem(len_item, 1, QTableWidgetItem(name))

        self.url_dict[idx] = url


class ImageTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(ImageTabWidget, self).__init__(parent)

