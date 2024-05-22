# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate, DSDelete
from core.database import DBManager
from core.weedfs import SeaWeedFS
from ui.widget import ImageTabInnerWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, cfg=None, logger=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.cfg = cfg
        self.logger = logger

        self.db_manager = DBManager(user=cfg.user,
                                    password=cfg.password,
                                    host=cfg.host,
                                    port=cfg.port,
                                    database=cfg.database,
                                    logger=logger)
        self.weed_manager = SeaWeedFS(cfg=cfg, logger=self.logger)

        # Set params
        self.cur_tab_idx = -1
        self.cur_tab_name = None

        # init drawing
        self.draw_dataset()
        self.draw_image_list_widget()

        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)

        self.tB_header_uploadImage.clicked.connect(self.insert_image)
        self.actionUpload_Image.triggered.connect(self.insert_image)
        self.tB_header_delDataset.clicked.connect(self.delete_dataset)
        self.actionDelete_Dataset.triggered.connect(self.delete_dataset)

        self.tW_img.currentChanged.connect(self.change_tab)

        self.tW_images.itemClicked.connect(self.draw_image)

        self.logger.info("Success initializing MainWindow")

    def create_dataset(self):
        ds_create = DSCreate(self, self.db_manager)
        ds_create.show()

        self.logger.info("Click 'dataset create'")

    def delete_dataset(self):
        cur_idx = self.tW_img.currentIndex()
        cur_tab_name = self.tW_img.tabText(cur_idx)

        q_delete = DSDelete(self, cur_tab_name, self.db_manager)
        q_delete.exec()

        self.logger.info("Click 'dataset delete'")

    def insert_image(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        fileDialog.setViewMode(QFileDialog.ViewMode.List)     # Detail, List
        # By default, all options are disabled.
        fileDialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        fileDialog.setOption(QFileDialog.Option.ReadOnly, True)
        fileDialog.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, True)
        fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

        fileNames = fileDialog.getOpenFileNames(
            parent=self,
            caption="Open Image",
            dir="",
            filter="Image Files (*.png *.jpg *.jpeg *.bmp)",
        )
        filenames, filters = fileNames
        if not filenames:
            return
        else:
            # get current tab dataset_id
            ret = self.db_manager.read_dataset_detail(self.cur_tab_name)[0]
            dataset_id = ret[0]

            for filename in filenames:
                ret = self.weed_manager.put_image_collection(image=filename, filename=filename)

                idx = self.db_manager.insert_image(
                    dataset_id=dataset_id,
                    filename=ret['filename'],
                    image_url=ret['url'],
                    width=ret['width'],
                    height=ret['height']
                )
                self.tW_images.add_image_list(idx, ret['filename'], ret['url'])

    def draw_dataset(self):
        ds = self.db_manager.read_dataset()

        for d in ds:
            ds_name = d[1]
            wg = ImageTabInnerWidget(self)
            self.tW_img.addTab(wg, ds_name)

        self.cur_tab_idx = self.tW_img.currentIndex()
        self.cur_tab_name = self.tW_img.tabText(self.cur_tab_idx)
        self.logger.info(f"Success drawing datasets - Current tab index, name: {self.cur_tab_idx}-{self.cur_tab_name}")

    def draw_image_list_widget(self):
        # get current tab dataset_id
        ret = self.db_manager.read_dataset_detail(self.cur_tab_name)[0]
        dataset_id = ret[0]

        images = self.db_manager.get_images_by_dataset_id(dataset_id)
        self.tW_images.draw_image_list(images)

        self.logger.info(f"Success drawing image_list - Current tab index, dataset_id, image_len: "
                         f"{self.cur_tab_idx}-{dataset_id}, {len(images)} images")

    def draw_image(self, item: QTableWidgetItem):
        img_idx = self.tW_images.item(item.row(), 0).text()
        image_url = self.tW_images.url_dict[int(img_idx)]

        img = self.weed_manager.get_image(url=image_url)

        cur_tab = self.tW_img.currentWidget()
        cur_tab.set_qpixmap(img.toqpixmap(), scale=False)

    def change_tab(self, index):
        self.cur_tab_idx = index
        self.cur_tab_name = self.tW_img.tabText(index)

        self.draw_image_list_widget()

        self.logger.info(f"Success changing tab index, name: {index}-{self.cur_tab_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # init config & logger
    set_config('./configs/config.yaml')
    _cfg = get_config()

    init_logger(_cfg)
    _logger = get_logger()

    window = MainWindow(cfg=_cfg, logger=_logger)
    window.show()

    sys.exit(app.exec())
