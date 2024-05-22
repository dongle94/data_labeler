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
