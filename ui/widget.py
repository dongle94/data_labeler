from math import sqrt
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget, QWidget, QVBoxLayout, QSizePolicy, \
    QApplication
from PySide6.QtGui import QPainter, QPaintEvent, QPolygon, QPen, QColor, QBrush, Qt, QPixmap, QImage, QKeyEvent

from ui.label import ImgLabel, BoxOverlayLabel
from utils.coord import get_box_point
from core.qt.shape import Shape


class ImageTabInnerWidget(QWidget):
    CREATE, EDIT = [0, 1]
    drawing_line_color = QColor(255, 0, 0)
    drawing_rect_color = QColor(255, 0, 0)
    CURSOR_DEFAULT = Qt.CursorShape.ArrowCursor
    CURSOR_POINT = Qt.CursorShape.PointingHandCursor
    CURSOR_DRAW = Qt.CursorShape.CrossCursor
    CURSOR_MOVE = Qt.CursorShape.ClosedHandCursor
    CURSOR_GRAB = Qt.CursorShape.OpenHandCursor

    epsilon = 24.0

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # self.bg_label = ImgLabel(self)

        self.pos_click = []
        self.boxes = []

        # layout = QVBoxLayout()
        # layout.addWidget(self.bg_label)
        # self.setLayout(layout)

        # Param
        self.mode = self.CREATE
        self.shapes = []
        self.current = None
        self.line = Shape(line_color=self.drawing_line_color)
        self.prev_point = QPointF()
        self.pixmap = QPixmap()
        self.scale = 1.0
        self.label_font_size = 8
        self.visible = {}
        self.hide_background = False
        self.draw_square = False

        # Inner param
        self._painter = QPainter()
        self._cursor = self.CURSOR_DEFAULT
        self._hide_background = False

        # Event
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)

    def is_visible(self, shape):
        return self.visible.get(shape, True)

    def is_drawing(self):
        return self.mode == self.CREATE

    def is_editing(self):
        return self.mode == self.EDIT

    def set_qpixmap(self, pixmap: QPixmap, scale=False):
        # self.bg_label.setPixmap(pixmap)
        # self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.bg_label.setScaledContents(scale)
        self.pixmap = pixmap

    def add_box(self):
        # TODO add box
        pt1, pt2 = get_box_point(self.pos_click[0], self.pos_click[1])
        self.bg_label.add_rectangle(pt1[0], pt1[1], pt2[0], pt2[1])
        # box_overlay = BoxOverlayLabel(self, [pt1, pt2])
        # self.bg_label.boxes.append(box_overlay)
        # self.layout.addWidget(box_overlay)
        # box_overlay.show()

    def mousePressEvent(self, event):
        if self.window().cur_image_idx == -1:
            return

        pos = self.transform_pos(event.position())

        # Left click event -> create box
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_drawing():
                self.handle_drawing(pos)
            else:       # editing
                pass

    def mouseMoveEvent(self, event):
        if self.window().cur_image_idx == -1:
            return

        pos = self.transform_pos(event.position())

        # Polygon drawing.
        if self.is_drawing():
            self.override_cursor(self.CURSOR_DRAW)
            if self.current:
                color = self.drawing_line_color
                if self.out_of_pixmap(pos):
                    size = self.pixmap.size()
                    clipped_x = min(max(0, pos.x()), size.width())
                    clipped_y = min(max(0, pos.y()), size.height())
                    pos = QPointF(clipped_x, clipped_y)
                elif len(self.current) > 1 and self.close_enough(pos, self.current[0]):
                    pass

                if self.draw_square:
                    pass
                else:
                    self.line[1] = pos

                self.line.line_color = color
                self.prev_point = QPointF()
                self.current.highlight_clear()
            else:
                self.prev_point = pos
            self.repaint()
            return

    def mouseReleaseEvent(self, event):
        pos = self.transform_pos(event.position())

        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_drawing():
                self.handle_drawing(pos)
            else:
                pass

    def handle_drawing(self, pos):
        if self.current and self.current.reach_max_points() is False:
            init_pos = self.current[0]
            min_x = init_pos.x()
            min_y = init_pos.y()
            target_pos = self.line[1]
            max_x = target_pos.x()
            max_y = target_pos.y()
            self.current.add_point(QPointF(max_x, min_y))
            self.current.add_point(target_pos)
            self.current.add_point(QPointF(min_x, max_y))
            self.finalize()
        elif not self.out_of_pixmap(pos):
            self.current = Shape()
            self.current.add_point(pos)
            self.line.points = [pos, pos]
            self.set_hiding()
            # self.drawingPolygon.emit(True)
            self.update()

    def set_hiding(self, enable=True):
        self._hide_background = self.hide_background if enable else False

    def paintEvent(self, event):
        if not self.pixmap:
            return super().paintEvent(event)

        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        p.scale(self.scale, self.scale)
        p.translate(self.offset_to_center())

        p.drawPixmap(0, 0, self.pixmap)
        Shape.scale = self.scale
        Shape.label_font_size = self.label_font_size
        for shape in self.shapes:
            if shape.selected and self.is_visible(shape):
                shape.fill = shape.selected
                shape.paint(p)
        if self.current:
            self.current.paint(p)
            self.line.paint(p)

        # Paint rect
        if self.current is not None and len(self.line) == 2:
            left_top = self.line[0]
            right_bottom = self.line[1]
            rect_width = right_bottom.x() - left_top.x()
            rect_height = right_bottom.y() - left_top.y()
            p.setPen(self.drawing_rect_color)
            brush = QBrush(Qt.BrushStyle.BDiagPattern)
            p.setBrush(brush)
            p.drawRect(left_top.x(), left_top.y(), rect_width, rect_height)
        # Paint Cross line
        if self.is_drawing() and not self.prev_point.isNull() and not self.out_of_pixmap(self.prev_point):
            p.setPen(QColor(0, 0, 0))
            p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), self.pixmap.height())
            p.drawLine(0, int(self.prev_point.y()), self.pixmap.width(), int(self.prev_point.y()))

        self.setAutoFillBackground(True)

        p.end()

    def transform_pos(self, point):
        p = point / self.scale - self.offset_to_center()
        return p

    def offset_to_center(self):
        s = self.scale
        area = self.size()
        w, h = self.pixmap.width(), self.pixmap.height()
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPointF(x, y)

    def out_of_pixmap(self, p):
        w, h = self.pixmap.width(), self.pixmap.height()
        return not (0 <= p.x() <= w and 0 <= p.y() <= h)

    def finalize(self):
        assert self.current
        if self.current.points[0] == self.current.points[-1]:
            self.current = None
            # self.drawPolygon.emit(False)
            self.update()
            return

        self.current.close()
        self.shapes.append(self.current)
        self.current = None
        self.set_hiding(False)
        self.newShape.emit()
        self.update()

    def close_enough(self, p1, p2):
        x, y = (p1 - p2).x(), (p1-p2).y()
        d = sqrt(x * x + y * y)
        return d < self.epsilon

    def current_cursor(self):
        cursor = QApplication.overrideCursor()
        if cursor is not None:
            cursor = cursor.shape()
        return cursor

    def override_cursor(self, cursor):
        self._cursor = cursor
        if self.current_cursor() is None:
            QApplication.setOverrideCursor(cursor)
        else:
            QApplication.changeOverrideCursor(cursor)


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

