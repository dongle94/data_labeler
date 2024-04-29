# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from utils.config import get_config, set_config
from utils.logger import init_logger, get_logger
from ui.ui_mainwindow import Ui_MainWindow
from ui.dialog import DSCreate
from core.database import DBManager


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

        # init drawing
        self.draw_dataset()


        # Signal and Slot
        self.tB_header_addDataset.clicked.connect(self.create_dataset)
        self.actionCreate_Dataset.triggered.connect(self.create_dataset)

    def create_dataset(self):
        ds_create = DSCreate(self, self.db_manager)
        ds_create.show()

    def draw_dataset(self):
        ds = self.db_manager.read_dataset()
        print(ds)

        # TODO create widget to add
        pass


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
