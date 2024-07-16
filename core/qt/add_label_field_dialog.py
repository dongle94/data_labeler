from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QMessageBox

from ui.ui_add_label_field import Ui_add_field


class AddLabelFieldDialog(QDialog, Ui_add_field):
    def __init__(self, parent=None, dataset_id=None, db=None):
        super(AddLabelFieldDialog, self).__init__(parent)
        self.setupUi(self)

        self.dataset_id = dataset_id
        self.db_manager = db

        # init
        self.cur_class_num = 0
        self.cur_class_edit = []
        self.set_visible_type(False)
        self.set_visible_fieldname(False)
        self.set_visible_class(False)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

        # trigger
        self.rb_boxes.clicked.connect(self.set_visible_type)
        self.rb_image.clicked.connect(self.set_visible_type2)

        self.rb_box.clicked.connect(self.set_box_type)
        self.rb_box.clicked.connect(self.check_box_duplication)
        self.rb_caption.clicked.connect(self.set_caption_type)
        self.rb_cls.clicked.connect(self.set_classification_type)

        self.lE_fieldname.textEdited.connect(self.check_fieldname)
        self.bt_add_cls.clicked.connect(self.add_class)
        self.bt_del_cls.clicked.connect(self.sub_class)

    def set_visible_type(self, visible: bool):
        """click boxes format, clean element below.

        Args:
            visible: (bool) whether element is visible or not

        Returns:

        """
        # type
        self.lb_type.setVisible(visible)
        self.gb_type.setVisible(visible)
        self.rb_box.setAutoExclusive(False)
        self.rb_caption.setAutoExclusive(False)
        self.rb_cls.setAutoExclusive(False)
        self.rb_box.setVisible(visible)
        self.rb_caption.setVisible(visible)
        self.rb_cls.setVisible(visible)
        self.rb_box.setChecked(False)
        self.rb_caption.setChecked(False)
        self.rb_cls.setChecked(False)
        self.rb_box.setAutoExclusive(True)
        self.rb_caption.setAutoExclusive(True)
        self.rb_cls.setAutoExclusive(True)

        # field name & classes
        self.set_visible_fieldname(False)
        self.set_visible_class(False)
        self.clean_formlayout()

        # Button
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def set_visible_type2(self, visible: bool):
        """click image format, clean element below.

        Args:
            visible: (bool) whether element is visible or not

        Returns:

        """
        # type
        self.lb_type.setVisible(visible)
        self.gb_type.setVisible(visible)
        self.rb_box.setAutoExclusive(False)
        self.rb_caption.setAutoExclusive(False)
        self.rb_cls.setAutoExclusive(False)
        self.rb_box.setVisible(False)
        self.rb_caption.setVisible(visible)
        self.rb_cls.setVisible(visible)
        self.rb_box.setChecked(False)
        self.rb_caption.setChecked(False)
        self.rb_cls.setChecked(False)
        self.rb_box.setAutoExclusive(True)
        self.rb_caption.setAutoExclusive(True)
        self.rb_cls.setAutoExclusive(True)

        # field name & classes
        self.set_visible_fieldname(False)
        self.set_visible_class(False)
        self.clean_formlayout()

        # Button
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def set_visible_fieldname(self, visible: bool):
        self.lb_fieldname.setVisible(visible)
        self.lE_fieldname.setVisible(visible)

    def set_visible_class(self, visible: bool):
        self.lb_class.setVisible(visible)
        self.cb_duplicate.setVisible(visible)
        self.bt_add_cls.setVisible(visible)
        self.bt_del_cls.setVisible(visible)

    def set_box_type(self):
        self.set_visible_fieldname(False)
        self.set_visible_class(True)
        self.cb_duplicate.setChecked(False)
        self.cb_duplicate.setEnabled(False)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.clean_formlayout()

    def set_caption_type(self):
        self.set_visible_fieldname(True)
        self.set_visible_class(False)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.clean_formlayout()
        self.check_fieldname(self.lE_fieldname.text())

    def set_classification_type(self):
        self.set_visible_fieldname(True)
        self.set_visible_class(True)
        self.cb_duplicate.setEnabled(True)

        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.clean_formlayout()

    def check_fieldname(self, text):
        if self.rb_caption.isChecked():
            if len(text.strip()):
                self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
            else:
                self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        elif self.rb_cls.isChecked():
            pass

    def add_class(self):
        lineedit = QLineEdit(self)
        lineedit.textEdited.connect(self.check_entire_classfield)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.cur_class_edit.append(lineedit)
        self.flo_classes.addRow(f"{self.cur_class_num}: ", lineedit)

        self.cur_class_num += 1

    def sub_class(self):
        last_idx = self.flo_classes.rowCount()
        if last_idx != 0:
            self.cur_class_edit.pop(-1)
            self.flo_classes.removeRow(last_idx-1)
            if self.cur_class_num >= 0:
                self.cur_class_num -= 1
        if self.flo_classes.rowCount() == 0:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def clean_formlayout(self):
        self.cur_class_num = 0
        self.cur_class_edit = []
        if self.flo_classes.rowCount() > 0:
            for i in range(self.flo_classes.rowCount()-1, -1, -1):
                self.flo_classes.removeRow(i)

    def check_entire_classfield(self):
        _lineedit = QLineEdit(self)
        for lineedit in self.cur_class_edit:
            if len(lineedit.text().strip()) == 0:
                self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
                return
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)

    def check_box_duplication(self):
        # check duplication boxes-box
        rets = self.db_manager.read_label_field_by_dataset_id(self.dataset_id)
        for ret in rets:
            data_format = ret[3]
            data_type = ret[4]
            if data_format == 0 and data_type == 0:     # boxes-box
                msgBox = QMessageBox()
                msgBox.setText("데이터 셋 당 박스 별 타입은 1개만 존재할 수 있습니다.")
                msgBox.exec()
                self.rb_box.setAutoExclusive(False)
                self.rb_box.setChecked(False)
                self.rb_box.setAutoExclusive(True)
                self.set_visible_class(False)
                return
