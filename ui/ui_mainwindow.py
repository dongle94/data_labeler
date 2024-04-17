# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(640, 360))
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionUpload_Image = QAction(MainWindow)
        self.actionUpload_Image.setObjectName(u"actionUpload_Image")
        self.actionUpload_folder = QAction(MainWindow)
        self.actionUpload_folder.setObjectName(u"actionUpload_folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hlo_header = QHBoxLayout()
        self.hlo_header.setObjectName(u"hlo_header")

        self.verticalLayout.addLayout(self.hlo_header)

        self.hlo_main = QHBoxLayout()
        self.hlo_main.setObjectName(u"hlo_main")
        self.vlo_letf = QVBoxLayout()
        self.vlo_letf.setObjectName(u"vlo_letf")
        self.lw_images = QListWidget(self.centralwidget)
        self.lw_images.setObjectName(u"lw_images")

        self.vlo_letf.addWidget(self.lw_images, 0, Qt.AlignLeft)

        self.hlo_lefttb = QHBoxLayout()
        self.hlo_lefttb.setObjectName(u"hlo_lefttb")
        self.tB_down = QToolButton(self.centralwidget)
        self.tB_down.setObjectName(u"tB_down")
        self.tB_down.setMouseTracking(False)
        icon = QIcon(QIcon.fromTheme(u"go-up"))
        self.tB_down.setIcon(icon)
        self.tB_down.setArrowType(Qt.UpArrow)

        self.hlo_lefttb.addWidget(self.tB_down)

        self.tB_up = QToolButton(self.centralwidget)
        self.tB_up.setObjectName(u"tB_up")
        icon1 = QIcon(QIcon.fromTheme(u"go-down"))
        self.tB_up.setIcon(icon1)
        self.tB_up.setArrowType(Qt.DownArrow)

        self.hlo_lefttb.addWidget(self.tB_up)

        self.tB_rm_img = QToolButton(self.centralwidget)
        self.tB_rm_img.setObjectName(u"tB_rm_img")
        icon2 = QIcon(QIcon.fromTheme(u"user-trash"))
        self.tB_rm_img.setIcon(icon2)

        self.hlo_lefttb.addWidget(self.tB_rm_img)


        self.vlo_letf.addLayout(self.hlo_lefttb)

        self.vlo_letf.setStretch(0, 24)
        self.vlo_letf.setStretch(1, 1)

        self.hlo_main.addLayout(self.vlo_letf)

        self.vlo_center = QVBoxLayout()
        self.vlo_center.setObjectName(u"vlo_center")

        self.hlo_main.addLayout(self.vlo_center)

        self.vlo_right = QVBoxLayout()
        self.vlo_right.setObjectName(u"vlo_right")
        self.vlo_right.setSizeConstraint(QLayout.SetMaximumSize)
        self.lw_labels = QListWidget(self.centralwidget)
        self.lw_labels.setObjectName(u"lw_labels")
        self.lw_labels.setEnabled(True)
        self.lw_labels.setMaximumSize(QSize(16777215, 16777215))

        self.vlo_right.addWidget(self.lw_labels, 0, Qt.AlignRight)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")

        self.vlo_right.addLayout(self.formLayout)

        self.pB_add_label = QPushButton(self.centralwidget)
        self.pB_add_label.setObjectName(u"pB_add_label")

        self.vlo_right.addWidget(self.pB_add_label)

        self.vlo_right.setStretch(0, 6)
        self.vlo_right.setStretch(1, 4)
        self.vlo_right.setStretch(2, 1)

        self.hlo_main.addLayout(self.vlo_right)

        self.hlo_main.setStretch(0, 1)
        self.hlo_main.setStretch(1, 8)
        self.hlo_main.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hlo_main)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 24)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuData.addAction(self.actionUpload_Image)
        self.menuData.addAction(self.actionUpload_folder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionUpload_Image.setText(QCoreApplication.translate("MainWindow", u"Upload Image", None))
        self.actionUpload_folder.setText(QCoreApplication.translate("MainWindow", u"Upload folder", None))
#if QT_CONFIG(tooltip)
        self.tB_down.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_down.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.tB_up.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_up.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.tB_rm_img.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_rm_img.setText("")
        self.pB_add_label.setText(QCoreApplication.translate("MainWindow", u"Add Label", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"Data", None))
    # retranslateUi

