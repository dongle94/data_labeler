import hashlib
from math import sqrt

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton, QFileDialog


def create_label(parent, text, alignment=None, stylesheet=None):
    q_label = QLabel(parent)
    q_label.setText(text)
    if alignment:
        q_label.setAlignment(alignment)
    if stylesheet:
        q_label.setStyleSheet(stylesheet)

    return q_label


def create_button_group(parent, horizontal=True, names=None, duplication=False, clicked_callback=None):
    gb = QGroupBox(parent)
    gb_lo = QHBoxLayout(gb) if horizontal else QVBoxLayout(gb)
    if names:
        for name in names:
            widget = QCheckBox(parent=gb) if duplication else QRadioButton(parent=gb)
            widget.setText(name)
            if clicked_callback:
                widget.clicked.connect(clicked_callback)
            gb_lo.addWidget(widget)
    return gb


def generate_color_by_text(text):
    s = text
    hash_code = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)
    r = int((hash_code / 255) % 255)
    g = int((hash_code / 65025) % 255)
    b = int((hash_code / 16581375) % 255)
    return QColor(r, g, b, 100)


def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())


def get_xyxy(points):
    x1, y1 = float('inf'), float('inf')
    x2, y2 = -1, -1

    for p in points:
        x, y = p.x(), p.y()
        x1, y1 = min(x1, x), min(y1, y)
        x2, y2 = max(x2, x), max(y2, y)
    return x1, y1, x2, y2


def xyxy_to_rel(points, size):
    x1, y1, x2, y2 = points
    w, h = size.width(), size.height()

    rel_x1, rel_y1 = round(x1 / w, 6), round(y1 / h, 6)
    rel_x2, rel_y2 = round(x2 / w, 6), round(y2 / h, 6)

    return rel_x1, rel_y1, rel_x2, rel_y2


def rel_to_xyxy(points, size):
    x1, y1, x2, y2 = points
    w, h = size.width(), size.height()

    abs_x1, abs_y1, abs_x2, abs_y2 = int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h)
    return abs_x1, abs_y1, abs_x2, abs_y2


def get_dir_dialog(parent=None):
    dir_dialog = QFileDialog(parent)
    dir_dialog.setFileMode(QFileDialog.FileMode.Directory)
    dir_dialog.setViewMode(QFileDialog.ViewMode.List)

    dir_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
    dir_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dir_dialog.setOption(QFileDialog.Option.ReadOnly, True)
    dir_dialog.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)
    dir_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

    return dir_dialog


def get_file_dialog(parent=None, multiple_files=False):
    filedialog = QFileDialog(parent)
    if multiple_files is True:
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    else:
        filedialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    filedialog.setViewMode(QFileDialog.ViewMode.List)

    # By default, all options are disabled.
    filedialog.setOption(QFileDialog.Option.ShowDirsOnly, False)
    filedialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    filedialog.setOption(QFileDialog.Option.ReadOnly, True)
    filedialog.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)
    filedialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

    return filedialog
