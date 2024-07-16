import numpy as np
from copy import copy
from PIL import ImageDraw

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, QRect, QSize, QEvent
from PySide6.QtGui import QPainter, QPaintEvent, QPen, QColor, QBrush, Qt, QPixmap, QImage, QPalette


class ImgLabel(QLabel):
    draw = Signal(np.ndarray)
    updateText = Signal(str)

    def __init__(self, parent, *args):
        super().__init__(parent=parent, *args)

        self.mouse_x, self.mouse_y = 0, 0

        self.bg_img = None

        self.boxes = []
        self.boxes_rect = []

    def add_rectangle(self, x1, y1, x2, y2):
        label_w, label_h = self.parent().width(), self.parent().height()
        l = int(x1 * label_w)
        t = int(y1 * label_h)
        w = int((x2 - x1) * label_w)
        h = int((y2 - y1) * label_h)
        rect = QRect(l, t, w, h)
        self.boxes_rect.append(rect)

    def mouseMoveEvent(self, event):
        if self.window().cur_image_db_idx == -1:
            return

        if self.bg_img is not None:
            self.mouse_x, self.mouse_y = event.pos().x(), event.pos().y()
            self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        if self.window().cur_image_db_idx == -1:
            return

        super().paintEvent(event)
        x, y = self.mouse_x, self.mouse_y
        label_w, label_h = self.size().width(), self.size().height()

        qp = QPainter()
        qp.begin(self)

        # Set Pen: Line color
        line_width = 1 + max(label_w, label_h) // 1000
        qp.setPen(
            QPen(QColor("black"),
                 line_width,
                 Qt.PenStyle.SolidLine,
                 Qt.PenCapStyle.SquareCap,
                 Qt.PenJoinStyle.MiterJoin)
        )

        # Draw line
        qp.drawLine(x, 0, x, label_h)
        qp.drawLine(0, y, label_w, y)

        # Set Pen: Line color
        qp.setPen(QPen(QColor(255, 0, 0),
                       line_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap, Qt.PenJoinStyle.MiterJoin))

        # Set Brush: Area color
        qp.setBrush(QBrush(QColor(196, 196, 196, 10)))

        # Draw rect
        for rect in self.boxes_rect:
            qp.drawRect(rect)

        qp.end()


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
