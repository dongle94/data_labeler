import sys
import json
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QLineEdit, QHBoxLayout, QFormLayout, QVBoxLayout, \
    QLabel, QCheckBox
from PySide6.QtCore import Qt, Signal

from utils.logger import get_logger
from ui.ui_dataset import Ui_DS_Create
from ui.ui_basic_dialog import Ui_Basic_Dialog
from ui.widget import ImageTabInnerWidget
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
        wg = ImageTabInnerWidget(self)
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


class DSDelete(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, ds_name="", weed=None, db=None):
        super(DSDelete, self).__init__(parent)
        self.setupUi(self)

        self.ds_name = ds_name
        self.weed_manager = weed
        self.db_manager = db
        self.logger = get_logger()

        self.label.setText(f"{ds_name} 데이터 셋을 삭제하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonBox.accepted.connect(self.delete_ds)
        self.buttonBox.rejected.connect(self.cancel)

    def delete_ds(self):
        tab_widget = self.parent().tW_images
        # Get All image url in that inner tab
        img_num = len(tab_widget.url_dict)

        # Delete All images in weedfs
        for db_idx, img_url in tab_widget.url_dict.items():
            self.weed_manager.delete_file(url=img_url)

        # delete dataset in database
        try:
            self.db_manager.delete_dataset(self.ds_name)
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setText(f"데이터 셋 삭제에 실패했습니다: {e}")
            msgBox.exec()
            return

        self.logger.info(f"데이터 셋 삭제: {self.ds_name} / 지워진 이미지 수: {img_num}")
        self.parent().tW_img.removeTab(self.parent().tW_img.currentIndex())

    def cancel(self):
        self.close()
        self.logger.info("데이터 셋 삭제 취소")


class ImageDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, image_num=0, weed=None, db=None):
        super(ImageDeleteDialog, self).__init__(parent)
        self.setupUi(self)

        self.weed_manager = weed
        self.db_manager = db
        self.logger = get_logger()

        self.label.setText(f"{image_num} 개의 이미지를 삭제 하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.buttonBox.accepted.connect(self.delete_images)
        self.buttonBox.rejected.connect(self.cancel)

    def delete_images(self):
        # Get DB Index
        db_idx = set()
        image_list_table_widget = self.parent().tW_images
        for item in image_list_table_widget.selectedItems():
            img_db_idx = image_list_table_widget.item(item.row(), 0).text()
            db_idx.add(img_db_idx)

        # Get Weedfs url
        for img_db_idx in db_idx:
            weedfs_url = image_list_table_widget.url_dict[int(img_db_idx)]

            # Delete Weedfs image
            ret = self.weed_manager.delete_file(url=weedfs_url)

            # Delete in DB Table
            if ret is True:
                self.db_manager.delete_image_by_image_id(img_db_idx)

        # Draw again
        self.parent().draw_image_list_widget()

    def cancel(self):
        self.close()
        self.logger.info("이미지 삭제 취소")


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

        self.parent().add_label_field(rowid, label_format, label_type, field_name, is_duplicate, json.loads(classes))
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


class DeleteLabelDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, label_info=None, db=None):
        super(DeleteLabelDialog, self).__init__(parent)
        self.setupUi(self)

        self.label_info = label_info
        self.db_manager = db
        self.logger = get_logger()

        # init
        self.field_dict = {}
        self.draw_init_ui()

        # trigger
        self.buttonBox.rejected.connect(self.cancel)
        self.buttonBox.accepted.connect(self.delete_label)

    def draw_init_ui(self):
        widget_item = self.verticalLayout.takeAt(0)
        q_label = widget_item.widget()
        q_label.deleteLater()

        hlo = QHBoxLayout()
        label = QLabel(self)
        label.setText("필드 명")
        label.setStyleSheet("font-weight: bold;")
        hlo.addWidget(label, 5, Qt.AlignmentFlag.AlignLeft)
        label = QLabel(self)
        label.setText("삭제 여부")
        label.setStyleSheet("font-weight: bold;")
        hlo.addWidget(label, 1, Qt.AlignmentFlag.AlignRight)
        self.verticalLayout.insertLayout(0, hlo)

        for idx, label_item in enumerate(self.label_info):
            hlo = QHBoxLayout()
            checkbox = QCheckBox(self)
            checkbox.setText("")
            label = QLabel(self)
            label.setText(label_item[1])
            hlo.addWidget(label, 5, Qt.AlignmentFlag.AlignLeft)
            hlo.addWidget(checkbox, 1, Qt.AlignmentFlag.AlignRight)
            self.verticalLayout.insertLayout(idx+1, hlo)

            self.field_dict[label_item[0]] = [checkbox, label_item[1]]

    def delete_label(self):
        print(self.field_dict)

    def cancel(self):
        self.logger.info("라벨 필드 삭제 취소")
