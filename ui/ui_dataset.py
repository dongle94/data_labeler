# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_DS_Create(object):
    def setupUi(self, DS_Create):
        if not DS_Create.objectName():
            DS_Create.setObjectName(u"DS_Create")
        DS_Create.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DS_Create)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DS_Create)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lE_dataset_name = QLineEdit(DS_Create)
        self.lE_dataset_name.setObjectName(u"lE_dataset_name")

        self.verticalLayout.addWidget(self.lE_dataset_name)

        self.label_2 = QLabel(DS_Create)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.hlo_dstype = QHBoxLayout()
        self.hlo_dstype.setObjectName(u"hlo_dstype")
        self.rB_dstype_image = QRadioButton(DS_Create)
        self.rB_dstype_image.setObjectName(u"rB_dstype_image")
        self.rB_dstype_image.setChecked(True)

        self.hlo_dstype.addWidget(self.rB_dstype_image)

        self.rB_dstype_Statistics = QRadioButton(DS_Create)
        self.rB_dstype_Statistics.setObjectName(u"rB_dstype_Statistics")

        self.hlo_dstype.addWidget(self.rB_dstype_Statistics)


        self.verticalLayout.addLayout(self.hlo_dstype)

        self.label_3 = QLabel(DS_Create)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.pTE_ds_desc = QPlainTextEdit(DS_Create)
        self.pTE_ds_desc.setObjectName(u"pTE_ds_desc")

        self.verticalLayout.addWidget(self.pTE_ds_desc)

        self.hlo_ds_bt = QHBoxLayout()
        self.hlo_ds_bt.setObjectName(u"hlo_ds_bt")
        self.pB_ds_cancel = QPushButton(DS_Create)
        self.pB_ds_cancel.setObjectName(u"pB_ds_cancel")

        self.hlo_ds_bt.addWidget(self.pB_ds_cancel)

        self.pB_ds_create = QPushButton(DS_Create)
        self.pB_ds_create.setObjectName(u"pB_ds_create")

        self.hlo_ds_bt.addWidget(self.pB_ds_create)


        self.verticalLayout.addLayout(self.hlo_ds_bt)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)
        self.verticalLayout.setStretch(5, 1)
        self.verticalLayout.setStretch(6, 1)

        self.retranslateUi(DS_Create)

        QMetaObject.connectSlotsByName(DS_Create)
    # setupUi

    def retranslateUi(self, DS_Create):
        DS_Create.setWindowTitle(QCoreApplication.translate("DS_Create", u"Form", None))
        self.label.setText(QCoreApplication.translate("DS_Create", u"Dataset Name", None))
        self.label_2.setText(QCoreApplication.translate("DS_Create", u"Dataset Type", None))
        self.rB_dstype_image.setText(QCoreApplication.translate("DS_Create", u"Image", None))
        self.rB_dstype_Statistics.setText(QCoreApplication.translate("DS_Create", u"Statistics", None))
        self.label_3.setText(QCoreApplication.translate("DS_Create", u"Dataset Description", None))
        self.pB_ds_cancel.setText(QCoreApplication.translate("DS_Create", u"Cancel", None))
        self.pB_ds_create.setText(QCoreApplication.translate("DS_Create", u"Create", None))
    # retranslateUi

