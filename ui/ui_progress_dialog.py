# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        if not ProgressDialog.objectName():
            ProgressDialog.setObjectName(u"ProgressDialog")
        ProgressDialog.setEnabled(True)
        ProgressDialog.resize(400, 200)
        ProgressDialog.setModal(False)
        self.verticalLayout_2 = QVBoxLayout(ProgressDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pD_label = QLabel(ProgressDialog)
        self.pD_label.setObjectName(u"pD_label")

        self.verticalLayout_2.addWidget(self.pD_label)

        self.pBar = QProgressBar(ProgressDialog)
        self.pBar.setObjectName(u"pBar")
        self.pBar.setEnabled(True)
        self.pBar.setValue(0)
        self.pBar.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pBar.setTextVisible(True)

        self.verticalLayout_2.addWidget(self.pBar)

        self.pB_close = QPushButton(ProgressDialog)
        self.pB_close.setObjectName(u"pB_close")
        self.pB_close.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pB_close.sizePolicy().hasHeightForWidth())
        self.pB_close.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.pB_close)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)

        self.retranslateUi(ProgressDialog)

        QMetaObject.connectSlotsByName(ProgressDialog)
    # setupUi

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(QCoreApplication.translate("ProgressDialog", u"Upload", None))
        self.pD_label.setText("")
        self.pB_close.setText(QCoreApplication.translate("ProgressDialog", u"Success", None))
    # retranslateUi

