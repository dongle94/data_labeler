import json
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QLineEdit
from PySide6.QtCore import Qt

from utils.logger import get_logger
from core.qt.inner_tab import ImageTabInnerWidget
from ui.ui_dataset import Ui_DS_Create
from ui.ui_add_label_field import Ui_add_field
from utils.checks import is_empty


class DSCreate(QDialog, Ui_DS_Create):
    def __init__(self, parent=None, db=None):
        super(DSCreate, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.db_manager = db
        self.logger = get_logger()

        # Signal & Slot
        self.pB_ds_create.clicked.connect(self.create_ds)
        self.pB_ds_cancel.clicked.connect(self.cancel)

    def create_ds(self):
        ds_name = self.lE_dataset_name.text()
        ds_type = self.get_ds_type()
        ds_desc = self.pTE_ds_desc.toPlainText()

        # check valid format
        if is_empty(ds_name) is True:
            msgBox = QMessageBox()
            msgBox.setText("데이터 셋 이름은 공백이 될 수 없습니다.")
            msgBox.exec()
            return

        # db search with ds_name
        res = self.db_manager.read_dataset_detail(ds_name)
        if len(res) != 0:
            msgBox = QMessageBox()
            msgBox.setText("이미 존재하는 데이터 셋 이름입니다.")
            msgBox.exec()
            return

        # db insert
        try:
            self.db_manager.create_dataset(ds_name, ds_type, ds_desc)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText(f"데이터 셋 생성에 실패했습니다: {e}")
            msgBox.exec()
            return

        msgBox = QMessageBox()
        msgBox.setText(f"데이터 셋 생성에 성공하였습니다.")
        msgBox.exec()
        self.accept()

        # (GUI)Draw dataset in tabWidget
        wg = ImageTabInnerWidget(self.parent())
        wg.newShape.connect(self.parent().draw_new_box_label)
        wg.selectionChanged.connect(self.parent().shape_selection_changed)
        self.parent().tW_img.addTab(wg, ds_name)

        # TODO add dataset desc

        self.logger.info(f"데이터 셋 생성: {ds_name}-{ds_type}-{ds_desc}")

    def cancel(self):
        self.close()
        self.logger.info("데이터 셋 생성 취소")

    def get_ds_type(self):
        if self.rB_dstype_image.isChecked():
            return 0
        elif self.rB_dstype_Statistics.isChecked():
            return 1


class AddLabelDialog(QDialog, Ui_add_field):
    def __init__(self, parent=None, dataset_id=None, db=None):
        super(AddLabelDialog, self).__init__(parent)
        self.setupUi(self)

        self.dataset_id = dataset_id
        self.db_manager = db
        self.logger = get_logger()

        # init
        self.cur_class_num = 0
        self.cur_class_edit = []
        self.set_visible_type(False)
        self.set_visible_fieldname(False)
        self.set_visible_class(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

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

        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.save_label)

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
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

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
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

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

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.clean_formlayout()

    def set_caption_type(self):
        self.set_visible_fieldname(True)
        self.set_visible_class(False)

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.clean_formlayout()
        self.check_fieldname(self.lE_fieldname.text())

    def set_classification_type(self):
        self.set_visible_fieldname(True)
        self.set_visible_class(True)
        self.cb_duplicate.setEnabled(True)

        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.clean_formlayout()

    def check_fieldname(self, text):
        if self.rb_caption.isChecked():
            if len(text.strip()):
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        elif self.rb_cls.isChecked():
            pass

    def add_class(self):
        lineedit = QLineEdit(self)
        lineedit.textEdited.connect(self.check_entire_classfield)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
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
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

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
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                return
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def save_label(self):
        label_format = 0  # 0: boxes, 1: images
        if self.rb_boxes.isChecked():
            label_format = 0
        elif self.rb_image.isChecked():
            label_format = 1

        label_type = 0      # 0: box, 1: caption, 2: classification
        if self.rb_box.isChecked():
            label_type = 0
        elif self.rb_caption.isChecked():
            label_type = 1
        elif self.rb_cls.isChecked():
            label_type = 2

        field_name = None
        if self.rb_caption.isChecked() or self.rb_cls.isChecked():
            field_name = self.lE_fieldname.text()

        is_duplicate = False
        if self.rb_cls.isChecked():
            is_duplicate = self.cb_duplicate.isChecked()

        classes = {}
        if self.rb_box.isChecked() or self.rb_cls.isChecked():
            for idx, line_edit in enumerate(self.cur_class_edit):
                classes[idx] = line_edit.text()
        classes = json.dumps(classes)

        rowid = self.db_manager.create_label_field(
            name=field_name,
            dataset_id=self.dataset_id,
            label_format=label_format,
            label_type=label_type,
            is_duplicate=is_duplicate,
            detail=classes
        )

        self.logger.info(f"라벨 필드 생성: {label_format}-{label_type} / label_field row: {rowid}")

        self.parent().draw_one_label_field(rowid, label_format, label_type, field_name, is_duplicate, json.loads(classes))
        self.logger.info(f"라벨 필드 재 출력")

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

    def cancel(self):
        self.logger.info("라벨 필드 추가 취소")
