# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_label_field.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_add_field(object):
    def setupUi(self, add_field):
        if not add_field.objectName():
            add_field.setObjectName(u"add_field")
        add_field.resize(400, 300)
        self.verticalLayout = QVBoxLayout(add_field)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_format = QLabel(add_field)
        self.lb_format.setObjectName(u"lb_format")
        self.lb_format.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.lb_format)

        self.gb_format = QGroupBox(add_field)
        self.gb_format.setObjectName(u"gb_format")
        self.horizontalLayout_2 = QHBoxLayout(self.gb_format)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rb_boxes = QRadioButton(self.gb_format)
        self.rb_boxes.setObjectName(u"rb_boxes")
#if QT_CONFIG(accessibility)
        self.rb_boxes.setAccessibleName(u"")
#endif // QT_CONFIG(accessibility)

        self.horizontalLayout_2.addWidget(self.rb_boxes)

        self.rb_image = QRadioButton(self.gb_format)
        self.rb_image.setObjectName(u"rb_image")

        self.horizontalLayout_2.addWidget(self.rb_image)


        self.verticalLayout.addWidget(self.gb_format)

        self.lb_type = QLabel(add_field)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.lb_type)

        self.gb_type = QGroupBox(add_field)
        self.gb_type.setObjectName(u"gb_type")
        self.horizontalLayout_3 = QHBoxLayout(self.gb_type)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.rb_box = QRadioButton(self.gb_type)
        self.rb_box.setObjectName(u"rb_box")

        self.horizontalLayout_3.addWidget(self.rb_box)

        self.rb_caption = QRadioButton(self.gb_type)
        self.rb_caption.setObjectName(u"rb_caption")

        self.horizontalLayout_3.addWidget(self.rb_caption)

        self.rb_cls = QRadioButton(self.gb_type)
        self.rb_cls.setObjectName(u"rb_cls")

        self.horizontalLayout_3.addWidget(self.rb_cls)


        self.verticalLayout.addWidget(self.gb_type)

        self.lb_fieldname = QLabel(add_field)
        self.lb_fieldname.setObjectName(u"lb_fieldname")
        self.lb_fieldname.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.lb_fieldname)

        self.lE_fieldname = QLineEdit(add_field)
        self.lE_fieldname.setObjectName(u"lE_fieldname")

        self.verticalLayout.addWidget(self.lE_fieldname)

        self.hlo_class = QHBoxLayout()
        self.hlo_class.setObjectName(u"hlo_class")
        self.lb_class = QLabel(add_field)
        self.lb_class.setObjectName(u"lb_class")

        self.hlo_class.addWidget(self.lb_class)

        self.cb_duplicate = QCheckBox(add_field)
        self.cb_duplicate.setObjectName(u"cb_duplicate")

        self.hlo_class.addWidget(self.cb_duplicate)

        self.bt_add_cls = QToolButton(add_field)
        self.bt_add_cls.setObjectName(u"bt_add_cls")

        self.hlo_class.addWidget(self.bt_add_cls)

        self.bt_del_cls = QToolButton(add_field)
        self.bt_del_cls.setObjectName(u"bt_del_cls")

        self.hlo_class.addWidget(self.bt_del_cls)


        self.verticalLayout.addLayout(self.hlo_class)

        self.flo_classes = QFormLayout()
        self.flo_classes.setObjectName(u"flo_classes")

        self.verticalLayout.addLayout(self.flo_classes)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(add_field)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(add_field)
        self.buttonBox.accepted.connect(add_field.accept)
        self.buttonBox.rejected.connect(add_field.reject)

        QMetaObject.connectSlotsByName(add_field)
    # setupUi

    def retranslateUi(self, add_field):
        add_field.setWindowTitle(QCoreApplication.translate("add_field", u"Dialog", None))
        self.lb_format.setText(QCoreApplication.translate("add_field", u"Format", None))
        self.gb_format.setTitle("")
        self.rb_boxes.setText(QCoreApplication.translate("add_field", u"Boxes", None))
        self.rb_image.setText(QCoreApplication.translate("add_field", u"Image", None))
        self.lb_type.setText(QCoreApplication.translate("add_field", u"Type", None))
        self.gb_type.setTitle("")
        self.rb_box.setText(QCoreApplication.translate("add_field", u"Box", None))
        self.rb_caption.setText(QCoreApplication.translate("add_field", u"Caption", None))
        self.rb_cls.setText(QCoreApplication.translate("add_field", u"Classification", None))
        self.lb_fieldname.setText(QCoreApplication.translate("add_field", u"Field Name", None))
        self.lb_class.setText(QCoreApplication.translate("add_field", u"Class", None))
        self.cb_duplicate.setText(QCoreApplication.translate("add_field", u"dupllicate", None))
        self.bt_add_cls.setText(QCoreApplication.translate("add_field", u"+", None))
        self.bt_del_cls.setText(QCoreApplication.translate("add_field", u"-", None))
    # retranslateUi

