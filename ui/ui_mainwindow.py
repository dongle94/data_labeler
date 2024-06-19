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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLayout, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

from ui.widget import (ImageTabWidget, ImagesTableWidget)

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
        self.actionCreate_Dataset = QAction(MainWindow)
        self.actionCreate_Dataset.setObjectName(u"actionCreate_Dataset")
        self.actionDelete_Dataset = QAction(MainWindow)
        self.actionDelete_Dataset.setObjectName(u"actionDelete_Dataset")
        self.actionDelete_Whole_Label = QAction(MainWindow)
        self.actionDelete_Whole_Label.setObjectName(u"actionDelete_Whole_Label")
        self.actionDelete_Selected_Image = QAction(MainWindow)
        self.actionDelete_Selected_Image.setObjectName(u"actionDelete_Selected_Image")
        self.actionDelete_Selected_Label = QAction(MainWindow)
        self.actionDelete_Selected_Label.setObjectName(u"actionDelete_Selected_Label")
        self.actionDelete_Current_Image = QAction(MainWindow)
        self.actionDelete_Current_Image.setObjectName(u"actionDelete_Current_Image")
        self.actionDeltete_Current_Label = QAction(MainWindow)
        self.actionDeltete_Current_Label.setObjectName(u"actionDeltete_Current_Label")
        self.actionObject_Detection_for_whole_Image = QAction(MainWindow)
        self.actionObject_Detection_for_whole_Image.setObjectName(u"actionObject_Detection_for_whole_Image")
        self.actionObject_Detection_for_selected_Image = QAction(MainWindow)
        self.actionObject_Detection_for_selected_Image.setObjectName(u"actionObject_Detection_for_selected_Image")
        self.actionObject_Detection_for_Current_Image = QAction(MainWindow)
        self.actionObject_Detection_for_Current_Image.setObjectName(u"actionObject_Detection_for_Current_Image")
        self.actionObject_Detection_for_whole_Image_without_remove_label = QAction(MainWindow)
        self.actionObject_Detection_for_whole_Image_without_remove_label.setObjectName(u"actionObject_Detection_for_whole_Image_without_remove_label")
        self.actionObject_Detection_for_selected_images = QAction(MainWindow)
        self.actionObject_Detection_for_selected_images.setObjectName(u"actionObject_Detection_for_selected_images")
        self.actionObject_Detection_for_current_image = QAction(MainWindow)
        self.actionObject_Detection_for_current_image.setObjectName(u"actionObject_Detection_for_current_image")
        self.actionClassification_for_entire_Images = QAction(MainWindow)
        self.actionClassification_for_entire_Images.setObjectName(u"actionClassification_for_entire_Images")
        self.actionClassification_for_Selected_Images = QAction(MainWindow)
        self.actionClassification_for_Selected_Images.setObjectName(u"actionClassification_for_Selected_Images")
        self.actionClassification_for_Current_Image = QAction(MainWindow)
        self.actionClassification_for_Current_Image.setObjectName(u"actionClassification_for_Current_Image")
        self.actionClassification_entire_bounding_boxes_of_all_images = QAction(MainWindow)
        self.actionClassification_entire_bounding_boxes_of_all_images.setObjectName(u"actionClassification_entire_bounding_boxes_of_all_images")
        self.actionClassification_entire_bounding_boxes_of_current_image = QAction(MainWindow)
        self.actionClassification_entire_bounding_boxes_of_current_image.setObjectName(u"actionClassification_entire_bounding_boxes_of_current_image")
        self.actionClassification_current_bounding_box_of_current_image = QAction(MainWindow)
        self.actionClassification_current_bounding_box_of_current_image.setObjectName(u"actionClassification_current_bounding_box_of_current_image")
        self.actionSave_label = QAction(MainWindow)
        self.actionSave_label.setObjectName(u"actionSave_label")
        self.actionCreate_Mode = QAction(MainWindow)
        self.actionCreate_Mode.setObjectName(u"actionCreate_Mode")
        self.actionEdit_Mode = QAction(MainWindow)
        self.actionEdit_Mode.setObjectName(u"actionEdit_Mode")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hlo_header = QHBoxLayout()
        self.hlo_header.setObjectName(u"hlo_header")
        self.hlo_header.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hlo_header.addItem(self.horizontalSpacer)

        self.tB_header_addDataset = QToolButton(self.centralwidget)
        self.tB_header_addDataset.setObjectName(u"tB_header_addDataset")
        icon = QIcon(QIcon.fromTheme(u"document-new"))
        self.tB_header_addDataset.setIcon(icon)

        self.hlo_header.addWidget(self.tB_header_addDataset)

        self.tB_header_uploadDir = QToolButton(self.centralwidget)
        self.tB_header_uploadDir.setObjectName(u"tB_header_uploadDir")
        icon1 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.tB_header_uploadDir.setIcon(icon1)

        self.hlo_header.addWidget(self.tB_header_uploadDir, 0, Qt.AlignRight)

        self.tB_header_uploadImage = QToolButton(self.centralwidget)
        self.tB_header_uploadImage.setObjectName(u"tB_header_uploadImage")

        self.hlo_header.addWidget(self.tB_header_uploadImage)

        self.tB_header_delDataset = QToolButton(self.centralwidget)
        self.tB_header_delDataset.setObjectName(u"tB_header_delDataset")
        icon2 = QIcon(QIcon.fromTheme(u"edit-delete"))
        self.tB_header_delDataset.setIcon(icon2)

        self.hlo_header.addWidget(self.tB_header_delDataset)

        self.tB_header_delLabels = QToolButton(self.centralwidget)
        self.tB_header_delLabels.setObjectName(u"tB_header_delLabels")

        self.hlo_header.addWidget(self.tB_header_delLabels)

        self.tB_header_delSelectedImage = QToolButton(self.centralwidget)
        self.tB_header_delSelectedImage.setObjectName(u"tB_header_delSelectedImage")

        self.hlo_header.addWidget(self.tB_header_delSelectedImage, 0, Qt.AlignRight)

        self.tB_header_delCurLabel = QToolButton(self.centralwidget)
        self.tB_header_delCurLabel.setObjectName(u"tB_header_delCurLabel")

        self.hlo_header.addWidget(self.tB_header_delCurLabel, 0, Qt.AlignRight)


        self.verticalLayout.addLayout(self.hlo_header)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.hlo_main = QHBoxLayout()
        self.hlo_main.setObjectName(u"hlo_main")
        self.hlo_main.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.vlo_letf = QVBoxLayout()
        self.vlo_letf.setObjectName(u"vlo_letf")
        self.vlo_letf.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.tW_images = ImagesTableWidget(self.centralwidget)
        self.tW_images.setObjectName(u"tW_images")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tW_images.sizePolicy().hasHeightForWidth())
        self.tW_images.setSizePolicy(sizePolicy)

        self.vlo_letf.addWidget(self.tW_images)

        self.hlo_lefttb = QHBoxLayout()
        self.hlo_lefttb.setObjectName(u"hlo_lefttb")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hlo_lefttb.addItem(self.horizontalSpacer_3)

        self.tB_img_up = QToolButton(self.centralwidget)
        self.tB_img_up.setObjectName(u"tB_img_up")
        self.tB_img_up.setMouseTracking(False)
        icon3 = QIcon(QIcon.fromTheme(u"go-up"))
        self.tB_img_up.setIcon(icon3)
        self.tB_img_up.setArrowType(Qt.UpArrow)

        self.hlo_lefttb.addWidget(self.tB_img_up, 0, Qt.AlignHCenter)

        self.tB_img_down = QToolButton(self.centralwidget)
        self.tB_img_down.setObjectName(u"tB_img_down")
        icon4 = QIcon(QIcon.fromTheme(u"go-down"))
        self.tB_img_down.setIcon(icon4)
        self.tB_img_down.setArrowType(Qt.DownArrow)

        self.hlo_lefttb.addWidget(self.tB_img_down, 0, Qt.AlignHCenter)

        self.tB_img_del = QToolButton(self.centralwidget)
        self.tB_img_del.setObjectName(u"tB_img_del")
        icon5 = QIcon(QIcon.fromTheme(u"user-trash"))
        self.tB_img_del.setIcon(icon5)

        self.hlo_lefttb.addWidget(self.tB_img_del)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hlo_lefttb.addItem(self.horizontalSpacer_2)

        self.hlo_lefttb.setStretch(1, 1)
        self.hlo_lefttb.setStretch(2, 1)

        self.vlo_letf.addLayout(self.hlo_lefttb)

        self.vlo_letf.setStretch(0, 24)
        self.vlo_letf.setStretch(1, 1)

        self.hlo_main.addLayout(self.vlo_letf)

        self.vlo_center = QVBoxLayout()
        self.vlo_center.setObjectName(u"vlo_center")
        self.tW_img = ImageTabWidget(self.centralwidget)
        self.tW_img.setObjectName(u"tW_img")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tW_img.sizePolicy().hasHeightForWidth())
        self.tW_img.setSizePolicy(sizePolicy1)

        self.vlo_center.addWidget(self.tW_img)


        self.hlo_main.addLayout(self.vlo_center)

        self.vlo_right = QVBoxLayout()
        self.vlo_right.setObjectName(u"vlo_right")
        self.vlo_right.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lw_labels = QListWidget(self.centralwidget)
        self.lw_labels.setObjectName(u"lw_labels")
        self.lw_labels.setEnabled(True)
        self.lw_labels.setMaximumSize(QSize(16777215, 16777215))

        self.vlo_right.addWidget(self.lw_labels)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.tb_box_up = QToolButton(self.centralwidget)
        self.tb_box_up.setObjectName(u"tb_box_up")
        self.tb_box_up.setArrowType(Qt.UpArrow)

        self.horizontalLayout.addWidget(self.tb_box_up, 0, Qt.AlignLeft)

        self.tb_box_down = QToolButton(self.centralwidget)
        self.tb_box_down.setObjectName(u"tb_box_down")
        self.tb_box_down.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.tb_box_down, 0, Qt.AlignHCenter)

        self.tb_box_rm = QToolButton(self.centralwidget)
        self.tb_box_rm.setObjectName(u"tb_box_rm")
        icon6 = QIcon(QIcon.fromTheme(u"list-remove"))
        self.tb_box_rm.setIcon(icon6)

        self.horizontalLayout.addWidget(self.tb_box_rm, 0, Qt.AlignRight)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.vlo_right.addLayout(self.horizontalLayout)

        self.vlo_label_field = QVBoxLayout()
        self.vlo_label_field.setObjectName(u"vlo_label_field")
        self.vlo_label_field.setSizeConstraint(QLayout.SetMinimumSize)
        self.vlo_img_label_field = QVBoxLayout()
        self.vlo_img_label_field.setObjectName(u"vlo_img_label_field")

        self.vlo_label_field.addLayout(self.vlo_img_label_field)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.vlo_label_field.addWidget(self.line_2)

        self.vlo_box_label_field = QVBoxLayout()
        self.vlo_box_label_field.setObjectName(u"vlo_box_label_field")

        self.vlo_label_field.addLayout(self.vlo_box_label_field)

        self.vlo_label_field.setStretch(0, 1)
        self.vlo_label_field.setStretch(2, 1)

        self.vlo_right.addLayout(self.vlo_label_field)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.pB_label_add = QPushButton(self.centralwidget)
        self.pB_label_add.setObjectName(u"pB_label_add")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pB_label_add.sizePolicy().hasHeightForWidth())
        self.pB_label_add.setSizePolicy(sizePolicy2)
        self.pB_label_add.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout_3.addWidget(self.pB_label_add)

        self.pB_label_edit = QPushButton(self.centralwidget)
        self.pB_label_edit.setObjectName(u"pB_label_edit")
        self.pB_label_edit.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout_3.addWidget(self.pB_label_edit)

        self.pB_label_del = QPushButton(self.centralwidget)
        self.pB_label_del.setObjectName(u"pB_label_del")
        self.pB_label_del.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout_3.addWidget(self.pB_label_del)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.vlo_right.addLayout(self.horizontalLayout_3)

        self.vlo_right.setStretch(0, 4)
        self.vlo_right.setStretch(1, 1)
        self.vlo_right.setStretch(2, 10)
        self.vlo_right.setStretch(3, 1)

        self.hlo_main.addLayout(self.vlo_right)

        self.hlo_main.setStretch(0, 1)
        self.hlo_main.setStretch(1, 8)
        self.hlo_main.setStretch(2, 1)

        self.verticalLayout.addLayout(self.hlo_main)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 29)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1280, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuInfer = QMenu(self.menubar)
        self.menuInfer.setObjectName(u"menuInfer")
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuInfer.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menuFile.addAction(self.actionCreate_Dataset)
        self.menuFile.addAction(self.actionUpload_Image)
        self.menuFile.addAction(self.actionUpload_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionDelete_Dataset)
        self.menuFile.addAction(self.actionDelete_Whole_Label)
        self.menuFile.addAction(self.actionDelete_Selected_Image)
        self.menuFile.addAction(self.actionDelete_Selected_Label)
        self.menuFile.addAction(self.actionDeltete_Current_Label)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_label)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuData.addAction(self.actionCreate_Mode)
        self.menuData.addAction(self.actionEdit_Mode)
        self.menuInfer.addAction(self.actionObject_Detection_for_whole_Image)
        self.menuInfer.addAction(self.actionObject_Detection_for_selected_Image)
        self.menuInfer.addAction(self.actionObject_Detection_for_Current_Image)
        self.menuInfer.addSeparator()
        self.menuInfer.addAction(self.actionObject_Detection_for_whole_Image_without_remove_label)
        self.menuInfer.addAction(self.actionObject_Detection_for_selected_images)
        self.menuInfer.addAction(self.actionObject_Detection_for_current_image)
        self.menuInfer.addSeparator()
        self.menuInfer.addAction(self.actionClassification_for_entire_Images)
        self.menuInfer.addAction(self.actionClassification_for_Selected_Images)
        self.menuInfer.addAction(self.actionClassification_for_Current_Image)
        self.menuInfer.addSeparator()
        self.menuInfer.addAction(self.actionClassification_entire_bounding_boxes_of_all_images)
        self.menuInfer.addAction(self.actionClassification_entire_bounding_boxes_of_current_image)
        self.menuInfer.addAction(self.actionClassification_current_bounding_box_of_current_image)

        self.retranslateUi(MainWindow)

        self.tW_img.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionUpload_Image.setText(QCoreApplication.translate("MainWindow", u"Upload Image", None))
        self.actionUpload_folder.setText(QCoreApplication.translate("MainWindow", u"Upload folder", None))
        self.actionCreate_Dataset.setText(QCoreApplication.translate("MainWindow", u"Create Dataset", None))
        self.actionDelete_Dataset.setText(QCoreApplication.translate("MainWindow", u"Delete Dataset", None))
        self.actionDelete_Whole_Label.setText(QCoreApplication.translate("MainWindow", u"Delete Whole Label", None))
        self.actionDelete_Selected_Image.setText(QCoreApplication.translate("MainWindow", u"Delete Selected Image", None))
        self.actionDelete_Selected_Label.setText(QCoreApplication.translate("MainWindow", u"Delete Selected Label", None))
        self.actionDelete_Current_Image.setText(QCoreApplication.translate("MainWindow", u"Delete Current Image", None))
        self.actionDeltete_Current_Label.setText(QCoreApplication.translate("MainWindow", u"Delete Current Label", None))
        self.actionObject_Detection_for_whole_Image.setText(QCoreApplication.translate("MainWindow", u"Object Detection for entire Images", None))
        self.actionObject_Detection_for_selected_Image.setText(QCoreApplication.translate("MainWindow", u"Object Detection for selected images", None))
        self.actionObject_Detection_for_Current_Image.setText(QCoreApplication.translate("MainWindow", u"Object Detection for Current Image", None))
        self.actionObject_Detection_for_whole_Image_without_remove_label.setText(QCoreApplication.translate("MainWindow", u"Object Detection for entire image without removing labels", None))
        self.actionObject_Detection_for_selected_images.setText(QCoreApplication.translate("MainWindow", u"Object Detection for Selected Images without removing labels", None))
        self.actionObject_Detection_for_current_image.setText(QCoreApplication.translate("MainWindow", u"Object Detection for Current Image without removing labels ", None))
        self.actionClassification_for_entire_Images.setText(QCoreApplication.translate("MainWindow", u"Classification for entire Images", None))
        self.actionClassification_for_Selected_Images.setText(QCoreApplication.translate("MainWindow", u"Classification for Selected Images", None))
        self.actionClassification_for_Current_Image.setText(QCoreApplication.translate("MainWindow", u"Classification for Current Image", None))
        self.actionClassification_entire_bounding_boxes_of_all_images.setText(QCoreApplication.translate("MainWindow", u"Classification entire bounding boxes of all images", None))
        self.actionClassification_entire_bounding_boxes_of_current_image.setText(QCoreApplication.translate("MainWindow", u"Classification entire bounding boxes of current image", None))
        self.actionClassification_current_bounding_box_of_current_image.setText(QCoreApplication.translate("MainWindow", u"Classification current bounding box of current image", None))
        self.actionSave_label.setText(QCoreApplication.translate("MainWindow", u"Save label", None))
        self.actionCreate_Mode.setText(QCoreApplication.translate("MainWindow", u"Create Mode", None))
        self.actionEdit_Mode.setText(QCoreApplication.translate("MainWindow", u"Edit Mode", None))
        self.tB_header_addDataset.setText(QCoreApplication.translate("MainWindow", u"AddDataset", None))
        self.tB_header_uploadDir.setText(QCoreApplication.translate("MainWindow", u"UploadDir", None))
        self.tB_header_uploadImage.setText(QCoreApplication.translate("MainWindow", u"UploadImage", None))
        self.tB_header_delDataset.setText(QCoreApplication.translate("MainWindow", u"DeleteDataset", None))
        self.tB_header_delLabels.setText(QCoreApplication.translate("MainWindow", u"DeleteLabels", None))
        self.tB_header_delSelectedImage.setText(QCoreApplication.translate("MainWindow", u"DeleteSelectedImage", None))
        self.tB_header_delCurLabel.setText(QCoreApplication.translate("MainWindow", u"DeleteCurLabel", None))
#if QT_CONFIG(tooltip)
        self.tB_img_up.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_img_up.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.tB_img_down.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_img_down.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.tB_img_del.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.tB_img_del.setText("")
        self.tb_box_up.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.tb_box_down.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.tb_box_rm.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pB_label_add.setText(QCoreApplication.translate("MainWindow", u"add", None))
        self.pB_label_edit.setText(QCoreApplication.translate("MainWindow", u"edit", None))
        self.pB_label_del.setText(QCoreApplication.translate("MainWindow", u"del", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"Data", None))
        self.menuInfer.setTitle(QCoreApplication.translate("MainWindow", u"Infer", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
    # retranslateUi

