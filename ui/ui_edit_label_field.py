# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_label_field.ui'
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
    QFrame, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 500)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.toolButton = QToolButton(Dialog)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton)

        self.toolButton_2 = QToolButton(Dialog)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setEnabled(False)

        self.horizontalLayout.addWidget(self.toolButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.toolButton_3 = QToolButton(Dialog)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButton_3)

        self.toolButton_4 = QToolButton(Dialog)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButton_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.line_3 = QFrame(Dialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.line_4 = QFrame(Dialog)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.toolButton_5 = QToolButton(Dialog)
        self.toolButton_5.setObjectName(u"toolButton_5")
        self.toolButton_5.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.toolButton_5)

        self.toolButton_6 = QToolButton(Dialog)
        self.toolButton_6.setObjectName(u"toolButton_6")
        self.toolButton_6.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.toolButton_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Boxes-box", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.toolButton_2.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Boxes-caption", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Boxes-cls", None))
        self.toolButton_3.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.toolButton_4.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Image-caption", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Image-cls", None))
        self.toolButton_5.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.toolButton_6.setText(QCoreApplication.translate("Dialog", u"-", None))
    # retranslateUi

