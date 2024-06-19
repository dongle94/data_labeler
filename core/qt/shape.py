import sys

from PySide6.QtGui import QColor, QPen, QPainterPath, QFont


class Shape(object):
    P_SQUARE, P_ROUND = 0, 1

    line_color = QColor(0, 255, 0, 128)
    fill_color = QColor(255, 0, 0, 128)
    select_line_color = QColor(255, 255, 255)
    select_fill_color = QColor(0, 128, 255, 155)
    vertex_fill_color = QColor(0, 255, 0, 255)
    point_type = P_SQUARE
    point_size = 16
    scale = 1.0
    label_font_size = 8

    def __init__(self, label=None, line_color=None, paint_label=False):
        self.label = label
        self.points = []
        self.fill = False
        self.selected = False
        self.paint_label = paint_label

        # Inner param
        self._closed = False

        self._highlight_index = None

        if line_color is not None:
            self.line_color = line_color

    def open(self):
        self._closed = False

    def close(self):
        self._closed = True

    def reach_max_points(self):
        if len(self.points) >= 4:
            return True
        return False

    def add_point(self, point):
        if not self.reach_max_points():
            self.points.append(point)

    def pop_point(self):
        if self.points:
            return self.points.pop()
        return None

    def is_closed(self):
        return self._closed

    def paint(self, painter):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QPainterPath()
            vertex_path = QPainterPath()

            line_path.moveTo(self.points[0])
            for i, p in enumerate(self.points):
                line_path.lineTo(p)
                self.draw_vertex(vertex_path, i)
            if self.is_closed():
                line_path.lineTo(self.points[0])

            painter.drawPath(line_path)
            painter.drawPath(vertex_path)
            painter.fillPath(vertex_path, self.vertex_fill_color)

            # Draw label text
            if self.paint_label:
                min_x = sys.maxsize
                min_y = sys.maxsize
                min_y_label = int(1.25 * self.label_font_size)
                for point in self.points:
                    min_x = min(min_x, point.x())
                    min_y = min(min_y, point.y())
                if min_x != sys.maxsize and min_y != sys.maxsize:
                    font = QFont()
                    font.setPointSize(self.label_font_size)
                    font.setBold(True)
                    painter.setFont(font)
                    if self.label is None:
                        self.label = ""
                    if min_y < min_y_label:
                        min_y += min_y_label
                    painter.drawText(min_x, min_y, self.label)

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)

    def draw_vertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]

        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def highlight_clear(self):
        self._highlight_index = None

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
