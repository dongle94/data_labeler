import requests
from urllib.parse import urlparse

from core.seaweedfs.util import *
from utils.logger import get_logger


class SeaWeedFS(object):
    def __init__(self, cfg=None, logger=None):
        url = get_normal_addr(cfg.weed_master_url)
        o = urlparse(url)
        self.master_url = url
        self.master_host = o.hostname
        self.master_port = o.port

        self.collection_name = cfg.weed_collection_name
        self.collection_count = cfg.weed_collection_count

        self.use_public_url = cfg.weed_use_public_url

        use_session = True

        self.logger = logger if logger is not None else get_logger()

    def get_status(self):
        url = f'http://{self.master_host}:{self.master_port}/dir/status'
        res = requests.get(url)
        if res.status_code != 200:
            res = res.json()
        else:
            res = res.json()
        return res

    def allocate_collection(self, collection_name="", count=1, **kwargs):
        params = '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        param = params if params else ""
        url = (f"http://{self.master_host}:{self.master_port}/vol/grow"
               f"?collection={self.collection_name}&count={self.collection_count}{param}")
        res = requests.get(url)
        if res.ok:
            return True
        else:
            return False

    def assign(self, params=None):
        param = "?" + params if params else ""
        url = f"http://{self.master_host}:{self.master_port}/dir/assign{param}"


if __name__ == '__main__':
    from utils.config import get_config, set_config
    set_config('./configs/config.yaml')
    _cfg = get_config()
    i = SeaWeedFS(cfg=_cfg)

    ret = i.get_status()
    print(ret)

    # ret = i.allocate_collection()
    # print(ret)