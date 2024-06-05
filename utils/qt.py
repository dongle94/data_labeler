
from PySide6.QtWidgets import QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, QCheckBox, QRadioButton


def create_label(parent, text, alignment=None, stylesheet=None):
    q_label = QLabel(parent)
    q_label.setText(text)
    if alignment:
        q_label.setAlignment(alignment)
    if stylesheet:
        q_label.setStyleSheet(stylesheet)

    return q_label


def create_button_group(parent, horizontal=True, names=None, duplication=False):
    gb = QGroupBox(parent)
    gb_lo = QHBoxLayout(gb) if horizontal else QVBoxLayout(gb)
    if names:
        for name in names:
            widget = QCheckBox(parent=gb) if duplication else QRadioButton(parent=gb)
            widget.setText(name)
            gb_lo.addWidget(widget)
    return gb


