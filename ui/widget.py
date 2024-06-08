from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPainter, QPaintEvent, QPolygon, QPen, QColor, QBrush, Qt, QPixmap, QImage, QKeyEvent

from ui.label import ImgLabel, BoxOverlayLabel
from utils.coord import get_box_point


class ImageTabInnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.bg_label = ImgLabel(self)

        self.pos_click = []
        self.boxes = []

        layout = QVBoxLayout()
        layout.addWidget(self.bg_label)
        self.setLayout(layout)

        # Event
        self.bg_label.setMouseTracking(True)

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
        self.boxes.append(BoxOverlayLabel())
        # TODO add box
        print(self.pos_click)

        pt1, pt2 = get_box_point(self.pos_click[0], self.pos_click[1])
        print(pt1, pt2)

    def mousePressEvent(self, event):
        if self.window().cur_image_idx == -1:
            return

        # Left click event -> create box
        if event.button() == Qt.MouseButton.LeftButton:
            rel_x, rel_y = self.get_rel_img_pos(event.position())
            self.pos_click.append([rel_x, rel_y])

            # create box
            if len(self.pos_click) == 2:
                self.add_box()
                self.pos_click = []

    def get_rel_img_pos(self, position):
        click_x, click_y = position.x(), position.y()
        offset_width = int((self.size().width() - self.bg_label.size().width())/2)
        offset_height = int((self.size().height() - self.bg_label.size().height())/2)
        x = 0
        y = 0
        if click_x < offset_width:
            x = 0
        elif offset_width <= click_x <= self.bg_label.size().width() + offset_width:
            x = int(click_x - offset_width)
        elif self.bg_label.size().width() + offset_width < click_x:
            x = self.bg_label.size().width()
        if click_y < offset_height:
            y = 0
        elif offset_height <= click_y <= self.bg_label.size().height() + offset_height:
            y = int(click_y - offset_height)
        elif self.bg_label.size().height() + offset_height < click_y:
            y = self.bg_label.size().height()

        return x / self.bg_label.size().width(), y / self.bg_label.size().height()


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

    def draw_image_list(self, images):
        self.setRowCount(len(images))

        self.fid_dict = {}
        self.url_dict = {}
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
            self.window().get_upper_image()
        elif Qt.Key.Key_Down == event.key():
            self.window().get_lower_image()


class ImageTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(ImageTabWidget, self).__init__(parent)

