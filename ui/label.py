import numpy as np
from copy import copy
from PIL import ImageDraw

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, QRect
from PySide6.QtGui import QPainter, QPaintEvent, QPolygon, QPen, QColor, QBrush, Qt, QPixmap, QImage


class ImgLabel(QLabel):
    draw = Signal(np.ndarray)
    updateText = Signal(str)

    def __init__(self, *args):
        super().__init__(*args)

        self.bg_img = None

    def mouseMoveEvent(self, event):
        if self.window().cur_image_idx == -1:
            return

        if self.bg_img is not None:
            x, y = event.pos().x(), event.pos().y()
            label_w, label_h = self.size().width(), self.size().height()
            img_w, img_h = self.bg_img.size
            abs_x, abs_y = int(x / label_w * img_w), int(y / label_h * img_h)
            img = copy(self.bg_img)
            draw = ImageDraw.Draw(img)

            draw.line((abs_x, 0, abs_x, img_h), fill=(0, 0, 0), width=1)
            draw.line((0, abs_y, img_w, abs_y), fill=(0, 0, 0), width=1)

            self.setPixmap(img.toqpixmap())


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
