from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QHBoxLayout, QLabel, QCheckBox

from utils.logger import get_logger
from ui.ui_basic_dialog import Ui_Basic_Dialog


class DatasetDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, dataset_name=""):
        super(DatasetDeleteDialog, self).__init__(parent)
        self.setupUi(self)

        self.label.setText(f"{dataset_name} 데이터 셋을 삭제하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


class ImagesDeleteDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, image_num=0):
        super(ImagesDeleteDialog, self).__init__(parent)
        self.setupUi(self)

        self.label.setText(f"{image_num} 개의 이미지를 삭제 하시겠습니까?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


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

    def draw_init_ui(self):
        widget_item = self.verticalLayout.takeAt(0)
        q_label = widget_item.widget()
        q_label.setParent(None)
        q_label.deleteLater()
        del q_label
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

    def cancel(self):
        self.logger.info("라벨 필드 삭제 취소")


class DetectionLabelsCreateDialog(QDialog, Ui_Basic_Dialog):
    def __init__(self, parent=None, weight="", img_num=0):
        super(DetectionLabelsCreateDialog, self).__init__(parent)
        self.setupUi(self)

        self.logger = get_logger()

        # init
        t = (f"디텍션 모델: {weight}\n"
             f"{img_num} 장의 이미지에 박스 라벨을 생성합니다.")
        self.label.setText(t)

        # trigger
        self.buttonBox.rejected.connect(self.cancel)

    def cancel(self):
        self.logger.info("디텍션 라벨 생성 취소")
