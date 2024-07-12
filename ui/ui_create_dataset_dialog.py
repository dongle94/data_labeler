# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_dataset_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.le_dataset_name = QLineEdit(Dialog)
        self.le_dataset_name.setObjectName(u"le_dataset_name")

        self.verticalLayout.addWidget(self.le_dataset_name)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.hlo_dstype = QHBoxLayout()
        self.hlo_dstype.setObjectName(u"hlo_dstype")
        self.rB_dstype_image = QRadioButton(Dialog)
        self.rB_dstype_image.setObjectName(u"rB_dstype_image")
        self.rB_dstype_image.setChecked(True)

        self.hlo_dstype.addWidget(self.rB_dstype_image)

        self.rB_dstype_Statistics = QRadioButton(Dialog)
        self.rB_dstype_Statistics.setObjectName(u"rB_dstype_Statistics")

        self.hlo_dstype.addWidget(self.rB_dstype_Statistics)


        self.verticalLayout.addLayout(self.hlo_dstype)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.te_ds_desc = QPlainTextEdit(Dialog)
        self.te_ds_desc.setObjectName(u"te_ds_desc")

        self.verticalLayout.addWidget(self.te_ds_desc)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Form", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Dataset Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Dataset Type", None))
        self.rB_dstype_image.setText(QCoreApplication.translate("Dialog", u"Image", None))
        self.rB_dstype_Statistics.setText(QCoreApplication.translate("Dialog", u"Statistics", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Dataset Description", None))
    # retranslateUi

