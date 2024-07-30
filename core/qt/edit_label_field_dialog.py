from PySide6.QtWidgets import QDialog, QHBoxLayout, QLineEdit

from utils.logger import get_logger
from utils.qt import create_label
from ui.ui_edit_label_field import Ui_Dialog


class EditLabelFieldDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None, dataset_id=None, db=None, label_info=None, *args, **kwargs):
        super(EditLabelFieldDialog, self).__init__(parent)
        self.setupUi(self)

        self.dataset_id = dataset_id
        self.db_manager = db
        self.label_info = label_info
        self.logger = get_logger()

        self.is_changed = False

        # init
        self.draw_init_ui()

    def draw_init_ui(self):
        bboxes = self.label_info.get('boxes-box')
        if bboxes:
            self.toolButton.setEnabled(True)
            self.toolButton_2.setEnabled(True)
            for cls_name, cls_idx in bboxes.items():
                cls_idx = int(cls_idx)
                t = f"{cls_idx}: "
                qlo = QHBoxLayout(self.parent())
                qle = QLineEdit(self.parent())
                qle.setText(cls_name)
                qlabel = create_label(self.parent(), t, stylesheet="color: gray")
                qlo.addWidget(qlabel)
                qlo.addWidget(qle)
                self.verticalLayout_2.addLayout(qlo)

    def add_boxes_box(self):
        pass

    def del_boxes_box(self):
        pass

    def add_boxes_cls(self):
        pass

    def del_boxes_cls(self):
        pass

    def add_img_cls(self):
        pass

    def del_img_cls(self):
        pass
