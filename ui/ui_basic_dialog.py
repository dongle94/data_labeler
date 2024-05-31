# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'basic_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Basic_Dialog(object):
    def setupUi(self, Basic_Dialog):
        if not Basic_Dialog.objectName():
            Basic_Dialog.setObjectName(u"Basic_Dialog")
        Basic_Dialog.resize(250, 150)
        self.verticalLayout = QVBoxLayout(Basic_Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Basic_Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(Basic_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Basic_Dialog)
        self.buttonBox.accepted.connect(Basic_Dialog.accept)
        self.buttonBox.rejected.connect(Basic_Dialog.reject)

        QMetaObject.connectSlotsByName(Basic_Dialog)
    # setupUi

    def retranslateUi(self, Basic_Dialog):
        Basic_Dialog.setWindowTitle(QCoreApplication.translate("Basic_Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Basic_Dialog", u"basic_text", None))
    # retranslateUi

