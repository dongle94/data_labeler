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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionUpload_Image = QAction(MainWindow)
        self.actionUpload_Image.setObjectName(u"actionUpload_Image")
        self.actionUpload_folder = QAction(MainWindow)
        self.actionUpload_folder.setObjectName(u"actionUpload_folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1281, 730))
        self.lo_cente = QHBoxLayout(self.horizontalLayoutWidget)
        self.lo_cente.setObjectName(u"lo_cente")
        self.lo_cente.setContentsMargins(0, 0, 0, 0)
        self.lw_images = QListWidget(self.horizontalLayoutWidget)
        self.lw_images.setObjectName(u"lw_images")

        self.lo_cente.addWidget(self.lw_images)

        self.tabWidget = QTabWidget(self.horizontalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(800, 0))
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.lo_cente.addWidget(self.tabWidget)

        self.lo_right = QVBoxLayout()
        self.lo_right.setObjectName(u"lo_right")
        self.lw_labels = QListWidget(self.horizontalLayoutWidget)
        self.lw_labels.setObjectName(u"lw_labels")
        self.lw_labels.setEnabled(True)
        self.lw_labels.setMinimumSize(QSize(0, 0))

        self.lo_right.addWidget(self.lw_labels)

        self.widget = QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 360))

        self.lo_right.addWidget(self.widget)


        self.lo_cente.addLayout(self.lo_right)

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionUpload_Image.setText(QCoreApplication.translate("MainWindow", u"Upload Image", None))
        self.actionUpload_folder.setText(QCoreApplication.translate("MainWindow", u"Upload folder", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"Data", None))
    # retranslateUi

