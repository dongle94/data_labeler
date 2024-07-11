from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QHBoxLayout, QLabel, QCheckBox

from utils.logger import get_logger
from ui.ui_basic_dialog import Ui_Basic_Dialog


class DatasetDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, ds_name="", weed=None, db=None):
        super(DatasetDeleteDialog, self).__init__(parent)
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


class ImagesDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, image_num=0, weed=None, db=None):
        super(ImagesDeleteDialog, self).__init__(parent)
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
            image_fid = image_list_table_widget.fid_dict[int(img_db_idx)]

            # Delete Weedfs image
            ret = self.weed_manager.delete_file(fid=image_fid)

            # Delete in DB Table
            if ret is True:
                self.db_manager.delete_image_data_by_image_id(img_db_idx)
                self.parent().statusbar.showMessage(f"Success delete image ")

        # Draw again
        self.parent().draw_image_list_widget()

    def cancel(self):
        self.close()
        self.logger.info("이미지 삭제 취소")


class LabelsFieldDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, label_info=None, db=None):
        super(LabelsFieldDeleteDialog, self).__init__(parent)
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
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

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
            checkbox.clicked.connect(self.valid_check_state)
            label = QLabel(self)
            label.setText(label_item[1])
            hlo.addWidget(label, 5, Qt.AlignmentFlag.AlignLeft)
            hlo.addWidget(checkbox, 1, Qt.AlignmentFlag.AlignRight)
            self.verticalLayout.insertLayout(idx+1, hlo)

            self.field_dict[label_item[0]] = [checkbox, label_item[1]]

    def valid_check_state(self):
        for _, item in self.field_dict.items():
            checkbox = item[0]
            if checkbox.isChecked():
                self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
                return
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)

    def delete_label(self):
        delete_field_name = []
        delete_idx = []
        for db_idx, label_item in self.field_dict.items():
            checkbox, label_field = label_item
            if checkbox.isChecked():
                delete_field_name.append(label_field)
                delete_idx.append(db_idx)

        # Remove in DB
        for idx in delete_idx:
            self.db_manager.delete_label_field_by_label_field_id(idx)

        text = f"'{delete_field_name.pop(0)}'"
        for label_field in delete_field_name:
            text += f", '{label_field}'"
        msgBox = QMessageBox()
        msgBox.setText(f"{len(delete_idx)}개의 필드 {text}을(를) 삭제하였습니다.")
        msgBox.exec()

        # Update UI
        self.parent().clean_label_field()
        self.parent().draw_label_field()

        self.logger.info(f"{len(delete_idx)}개의 라벨 필드 삭제: {delete_idx}")

    def cancel(self):
        self.logger.info("라벨 필드 삭제 취소")
