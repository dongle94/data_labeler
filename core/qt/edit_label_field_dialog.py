from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QToolButton

from utils.logger import get_logger
from utils.qt import create_label
from ui.ui_edit_label_field import Ui_Dialog


class EditLabelFieldDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None, label_info=None, *args, **kwargs):
        super(EditLabelFieldDialog, self).__init__(parent)
        self.setupUi(self)

        self.label_info = label_info
        self.logger = get_logger()

        self.is_changed = False

        # init
        self.orig_label_field = {}
        self.cur_label_field = {}
        self.boxes_box_cls_num = 0
        self.img_classes_cls_num = {}
        self.line_edits = []
        self.draw_init_ui()

        # Signal & slots
        self.toolButton.clicked.connect(self.add_boxes_box)
        self.toolButton_2.clicked.connect(self.del_boxes_box)
        self.toolButton_3.clicked.connect(self.add_boxes_cls)
        self.toolButton_4.clicked.connect(self.del_boxes_cls)

    def draw_init_ui(self):
        bboxes = self.label_info.get('boxes-box')
        self.orig_label_field['boxes-box'] = {}
        self.cur_label_field['boxes-box'] = {}
        if bboxes:
            self.toolButton.setEnabled(True)
            self.toolButton_2.setEnabled(True)
            for cls_name, cls_idx in bboxes.items():
                cls_idx = int(cls_idx)
                t = f"{cls_idx}: "
                qlo = QHBoxLayout()
                qle = QLineEdit(self.parent())
                qle.original_text = cls_name
                qle.setText(cls_name)
                self.line_edits.append(qle)
                qle.textChanged.connect(self.check_cls_change)
                qle.textEdited.connect(lambda s, x=qle: self.change_boxes_box_cls(x, x.text()))
                qlabel = create_label(self.parent(), t, stylesheet="color: gray")
                qlo.addWidget(qlabel)
                qlo.addWidget(qle)
                self.verticalLayout_2.addLayout(qlo)
                self.orig_label_field['boxes-box'][qle] = cls_name
                self.cur_label_field['boxes-box'][qle] = cls_name
                self.boxes_box_cls_num += 1

        img_caps = self.label_info.get('image-caption')
        self.orig_label_field['image-caption'] = {}
        self.cur_label_field['image-caption'] = {}
        for cap_field_name in img_caps:
            qle = QLineEdit(self.parent())
            qle.original_text = cap_field_name
            qle.setText(cap_field_name)
            qle.textChanged.connect(self.check_cls_change)
            qle.textEdited.connect(lambda s, x=qle: self.change_img_cap_field_name(x, x.text()))
            self.line_edits.append(qle)
            self.verticalLayout_5.addWidget(qle)
            self.orig_label_field['image-caption'][qle] = cap_field_name
            self.cur_label_field['image-caption'][qle] = cap_field_name

        img_cls = self.label_info.get('image-cls')
        self.orig_label_field['image-cls'] = {}
        self.cur_label_field['image-cls'] = {}
        for cls_field_name, cls_info in img_cls.items():
            vlo = QVBoxLayout()
            vlo.field_name = cls_field_name
            t = f"Image-classification: {cls_field_name}"
            self.img_classes_cls_num[cls_field_name] = 0
            qlo = QHBoxLayout()
            qlabel = create_label(self.parent(), t, stylesheet="color: navy")
            qlo.addWidget(qlabel)
            bt1 = QToolButton()
            bt1.setText('+')
            qlo.addWidget(bt1)
            bt2 = QToolButton()
            bt2.setText('-')
            bt1.clicked.connect(lambda s, x=vlo, y=bt2: self.add_img_cls(x, y))
            bt2.clicked.connect(lambda s, x=vlo, y=bt2: self.del_img_cls(x, y))
            qlo.addWidget(bt2)
            vlo.addLayout(qlo)
            self.orig_label_field['image-cls'][cls_field_name] = {}
            self.cur_label_field['image-cls'][cls_field_name] = {}
            for cls_name, cls_idx in cls_info.items():
                cls_idx = int(cls_idx)
                t = f"{cls_idx}: "
                qlo = QHBoxLayout()
                qle = QLineEdit(self.parent())
                qle.original_text = cls_name
                qle.setText(cls_name)
                self.line_edits.append(qle)
                qle.textChanged.connect(self.check_cls_change)
                qle.textEdited.connect(lambda s, x=cls_field_name, y=qle: self.change_img_cls(x, y, y.text()))
                qlabel = create_label(self.parent(), t, stylesheet="color: gray")
                qlo.addWidget(qlabel)
                qlo.addWidget(qle)
                vlo.addLayout(qlo)
                self.orig_label_field['image-cls'][cls_field_name][qle] = cls_name
                self.cur_label_field['image-cls'][cls_field_name][qle] = cls_name
                self.img_classes_cls_num[cls_field_name] += 1
            self.verticalLayout_6.addLayout(vlo)

    def add_boxes_box(self):
        t = f"{self.boxes_box_cls_num}: "
        qlo = QHBoxLayout()
        qle = QLineEdit(self.parent())
        qle.textEdited.connect(lambda s, x=qle: self.change_boxes_box_cls(x, x.text()))
        qlabel = create_label(self.parent(), t, stylesheet="color: gray")
        qlo.addWidget(qlabel)
        qlo.addWidget(qle)
        self.verticalLayout_2.addLayout(qlo)
        self.cur_label_field['boxes-box'][qle] = ""
        self.boxes_box_cls_num += 1
        if self.boxes_box_cls_num != 0:
            self.toolButton_2.setEnabled(True)

    def del_boxes_box(self):
        layout = self.verticalLayout_2.children()[self.boxes_box_cls_num]
        for c in range(layout.count()):
            w = self.verticalLayout_2.children()[self.boxes_box_cls_num].itemAt(c).widget()
            # w.deleteLater()       # deleteLater makes problem for refer in main
            w.hide()
            if isinstance(w, QLineEdit):
                del self.cur_label_field['boxes-box'][w]
        layout.deleteLater()
        layout.setParent(None)
        self.boxes_box_cls_num -= 1
        if self.boxes_box_cls_num == 0:
            self.toolButton_2.setEnabled(False)

    def add_boxes_cls(self):
        print("클릭 boxes-cls 클래스 추가")

    def del_boxes_cls(self):
        print("클릭 boxes-cls 클래스 삭제")

    def add_img_cls(self, vlo, bt):
        field_name = vlo.field_name
        t = f"{self.img_classes_cls_num[field_name]}: "
        qlo = QHBoxLayout()
        qle = QLineEdit(self.parent())
        qle.textEdited.connect(lambda s, x=qle: self.change_img_cls(field_name, x, x.text()))
        qlabel = create_label(self.parent(), t, stylesheet="color: gray")
        qlo.addWidget(qlabel)
        qlo.addWidget(qle)
        vlo.addLayout(qlo)
        self.cur_label_field['image-cls'][field_name][qle] = ""
        self.img_classes_cls_num[field_name] += 1
        if self.img_classes_cls_num[field_name] != 0:
            bt.setEnabled(True)

    def del_img_cls(self, vlo, bt):
        field_name = vlo.field_name

        layout = vlo.children()[self.img_classes_cls_num[field_name]]
        for c in range(layout.count()):
            w = vlo.children()[self.img_classes_cls_num[field_name]].itemAt(c).widget()
            # w.deleteLater()       # deleteLater makes problem for refer in main
            w.hide()
            if isinstance(w, QLineEdit):
                del self.cur_label_field['image-cls'][field_name][w]
        layout.deleteLater()
        layout.setParent(None)
        self.img_classes_cls_num[field_name] -= 1
        if self.img_classes_cls_num[field_name] == 0:
            bt.setEnabled(False)

    def check_cls_change(self, _):
        for le in self.line_edits:
            if le.original_text != le.text():
                self.is_changed = True
                return
        self.is_changed = False

    def change_boxes_box_cls(self, item, cls_name):
        self.cur_label_field['boxes-box'][item] = cls_name

    def change_img_cap_field_name(self, item, field_name):
        self.cur_label_field['image-caption'][item] = field_name

    def change_img_cls(self, label_name, item, cls_name):
        self.cur_label_field['image-cls'][label_name][item] = cls_name
