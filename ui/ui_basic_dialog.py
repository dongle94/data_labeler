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

class Ui_DS_Delete(object):
    def setupUi(self, DS_Delete):
        if not DS_Delete.objectName():
            DS_Delete.setObjectName(u"DS_Delete")
        DS_Delete.resize(250, 150)
        self.verticalLayout = QVBoxLayout(DS_Delete)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DS_Delete)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(DS_Delete)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DS_Delete)
        self.buttonBox.accepted.connect(DS_Delete.accept)
        self.buttonBox.rejected.connect(DS_Delete.reject)

        QMetaObject.connectSlotsByName(DS_Delete)
    # setupUi

    def retranslateUi(self, DS_Delete):
        DS_Delete.setWindowTitle(QCoreApplication.translate("DS_Delete", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("DS_Delete", u"basic_text", None))
    # retranslateUi

