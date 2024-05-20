# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate, DSDelete
from core.database import DBManager
from ui.imglabel import ImgWidget


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

        # Set params
        self.cur_tab_idx = -1
        self.cur_tab_name = None

        # init drawing
        self.draw_dataset()

        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)
        self.tB_header_delDataset.clicked.connect(self.delete_dataset)
        self.actionDelete_Dataset.triggered.connect(self.delete_dataset)

        self.tW_img.currentChanged.connect(self.change_tab)

        self.logger.info("Success initializing MainWindow")

    def create_dataset(self):
        ds_create = DSCreate(self, self.db_manager)
        ds_create.show()

        self.logger.info("Click 'dataset create'")

    def draw_dataset(self):
        ds = self.db_manager.read_dataset()

        for d in ds:
            ds_name = d[1]
            wg = ImgWidget(self)
            self.tW_img.addTab(wg, ds_name)

        # TODO add dataset current desc
        self.cur_tab_idx = self.tW_img.currentIndex()
        self.cur_tab_name = self.tW_img.tabText(self.cur_tab_idx)
        self.logger.info(f"Success drawing datasets - Current tab index, name: {self.cur_tab_idx}-{self.cur_tab_name}")

    def delete_dataset(self):
        cur_idx = self.tW_img.currentIndex()
        cur_tab_name = self.tW_img.tabText(cur_idx)

        q_delete = DSDelete(self, cur_tab_name, self.db_manager)
        q_delete.exec()

        self.logger.info("Click 'dataset delete'")

    def change_tab(self, index):
        self.cur_tab_idx = index
        self.cur_tab_name = self.tW_img.tabText(index)

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
