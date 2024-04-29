import numpy

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, QRect
from PySide6.QtGui import QPainter, QPaintEvent, QPolygon, QPen, QColor, QBrush, Qt, QPixmap, QImage


class ImgLabel(QLabel):
    draw = Signal(numpy.ndarray)
    updateText = Signal(str)

    def __init__(self, *args):
        super().__init__(*args)


class BoxOverlayLabel(ImgLabel):
    def __init__(self):
        super().__init__()

        self.box_points = []

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        qp = QPainter()
        qp.begin(self)

        # Set Pen: Line color
        qp.setPen(QPen(QColor(255, 0, 0),
                       2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap, Qt.PenJoinStyle.MiterJoin))

        # Set Brush: Area color
        qp.setBrush(QBrush(QColor(196, 196, 196, 96)))

        # Draw rect
        rect = QRect(self.box_points[0], self.box_points[1])
        qp.drawRect(rect)

        qp.end()


class ImgWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.bg_label = ImgLabel()

        layout = QVBoxLayout()
        self.img_labels = []
        layout.addWidget(self.bg_label)

        self.setLayout(layout)

    def set_image(self, img, scale=False):
        self.bg_label.setPixmap(QPixmap().fromImage(img))
        self.bg_label.setScaledContents(scale)

    def set_array(self, arr, scale=False):
        img = QImage(arr.data, arr.shape[1], arr.shape[0], QImage.Format.Format_BGR888)
        self.set_image(img)
        self.bg_label.setScaledContents(scale)

    def set_file(self, path, scale=False):
        qpixmap = QPixmap().load(path)
        self.bg_label.setPixmap(qpixmap)
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_label.setScaledContents(scale)

    def add_box(self):
        self.img_labels.append(BoxOverlayLabel())
        # TODO add box
