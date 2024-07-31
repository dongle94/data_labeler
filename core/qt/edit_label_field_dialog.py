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
        self.orig_label_field = {}
        self.cur_label_field = {}
        self.line_edits = []
        self.draw_init_ui()

        # Signal & slots
        self.toolButton.clicked.connect(self.add_boxes_box)
        self.toolButton_2.clicked.connect(self.del_boxes_box)
        self.toolButton_3.clicked.connect(self.add_boxes_cls)
        self.toolButton_4.clicked.connect(self.del_boxes_cls)
        self.toolButton_5.clicked.connect(self.add_img_cls)
        self.toolButton_6.clicked.connect(self.del_img_cls)

        print(label_info)

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
                qlabel = create_label(self.parent(), t, stylesheet="color: gray")
                qlo.addWidget(qlabel)
                qlo.addWidget(qle)
                self.verticalLayout_2.addLayout(qlo)
                self.orig_label_field['boxes-box'][qle] = cls_name
                self.cur_label_field['boxes-box'][qle] = cls_name

        img_caps = self.label_info.get('image-caption')
        self.orig_label_field['image-caption'] = {}
        self.cur_label_field['image-caption'] = {}
        for cap_field_name in img_caps:
            qle = QLineEdit(self.parent())
            qle.original_text = cap_field_name
            qle.setText(cap_field_name)
            qle.textChanged.connect(self.check_cls_change)
            self.line_edits.append(qle)
            self.verticalLayout_5.addWidget(qle)
            self.orig_label_field['image-caption'][qle] = cap_field_name
            self.cur_label_field['image-caption'][qle] = cap_field_name

        img_cls = self.label_info.get('image-cls')
        self.orig_label_field['image-cls'] = {}
        self.cur_label_field['image-cls'] = {}
        for cls_field_name, cls_info in img_cls.items():
            t = f"Image-classification: {cls_field_name}"
            qlabel = create_label(self.parent(), t, stylesheet="color: navy")
            self.verticalLayout_6.addWidget(qlabel)
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
                qlabel = create_label(self.parent(), t, stylesheet="color: gray")
                qlo.addWidget(qlabel)
                qlo.addWidget(qle)
                self.verticalLayout_6.addLayout(qlo)
                self.orig_label_field['image-cls'][cls_field_name][qle] = cls_name
                self.cur_label_field['image-cls'][cls_field_name][qle] = cls_name

    def add_boxes_box(self):
        print("클릭 boxes-box 클래스 추가")

    def del_boxes_box(self):
        print("클릭 boxes-box 클래스 삭제")

    def add_boxes_cls(self):
        print("클릭 boxes-cls 클래스 추가")

    def del_boxes_cls(self):
        print("클릭 boxes-cls 클래스 삭제")

    def add_img_cls(self):
        print("클릭 image-cls 클래스 추가")

    def del_img_cls(self):
        print("클릭 image-cls 클래스 삭제")

    def check_cls_change(self, _):
        for le in self.line_edits:
            if le.original_text != le.text():
                self.is_changed = True
                return
        self.is_changed = False
