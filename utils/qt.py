import hashlib

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton


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

