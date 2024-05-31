import os
import sys
import io
import numpy as np
from PIL import Image
from urllib.parse import urlparse

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from core.util import *
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

        self.init_collection()

    def get_status(self):
        url = f'http://{self.master_host}:{self.master_port}/dir/status'
        res = requests.get(url)
        if res.status_code != 200:
            res = res.json()
        else:
            res = res.json()
        return res

    def get_volume_status(self):
        url = f"http://{self.master_host}:{self.master_port}/vol/status"
        res = requests.get(url)
        if res.status_code != 200:
            res = res.json()
        else:
            res = res.json()
        return res

    def get_writable_collection(self):
        res = self.get_status()
        layouts = res['Topology'].get('layouts') or res['Topology'].get('Layouts')
        return layouts[0].get('collection')

    def init_collection(self):
        """
        1. get current volume collection info
        2. check available collection status
        3. do nothing or create collection

        :return:
        """
        weed_status = self.get_status()
        layouts = weed_status['Topology'].get('Layouts')
        if layouts is not None:
            pass
        else:
            _ = self.allocate_collection()

        weed_status = self.get_status()
        layouts = weed_status['Topology'].get('Layouts')
        self.logger.info(f"Success init collection: {layouts}")

    def allocate_collection(self, **kwargs):
        params = '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        param = params if params else ""
        url = (f"http://{self.master_host}:{self.master_port}/vol/grow"
               f"?collection={self.collection_name}&count={self.collection_count}{param}")
        res = requests.get(url)
        if res.ok:
            return True
        else:
            return False

    def assign(self, **kwargs):
        params = '&'.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
        param = "?" + params if params else ""
        url = f"http://{self.master_host}:{self.master_port}/dir/assign{param}"
        res = requests.get(url)

        if not res.ok:
            self.logger.error(f"assign got error: {res.status_code} - {res.get('error')}")
            return

        res = res.json()
        return res

    def put_image_collection(self, image, filename, data=None, **kwargs):
        collection = {"collection": self.get_writable_collection()}
        kwargs = {**kwargs, **collection}

        return self.put_image(image, filename=filename, data=data, **kwargs)

    def put_image(self, image, filename=None, data=None, **kwargs):
        im = image
        if isinstance(image, (np.ndarray, np.generic)):
            width, height = image.shape[1], image.shape[0]
            im = image[..., ::-1]
            im = Image.fromarray(im)
            out = io.BytesIO()
            if im.mode == 'RGBA':
                im.save(out, format='PNG')
                filename = os.path.splitext(filename)[0] + '.png'
            else:
                im.save(out, format='JPEG')
            out.seek(0)
        elif isinstance(im, Image.Image):
            width, height = im.size
            out = io.BytesIO()
            if im.mode == 'RGBA':
                im.save(out, format='PNG')
                filename = os.path.splitext(filename)[0] + '.png'
            else:
                im.save(out, format='JPEG')
            out.seek(0)
        else:
            im = Image.open(filename)
            width, height = im.size
            with open(filename, 'rb') as f:
                out = f.read()

        filename = os.path.basename(filename)

        res = self.put_file(stream=out, filename=filename, data=data, **kwargs)
        res['width'] = width
        res['height'] = height

        return res

    def put_file(self, path=None, stream=None, filename=None, data=None, **kwargs):
        res = self.assign(**kwargs)

        url = res["publicUrl" if self.use_public_url else "url"]
        fid = res["fid"]
        post_url = f"http://{url}/{fid}"

        filename = os.path.basename(path) if filename is None else filename
        if path is not None:
            files = {filename: open(path, "rb")}
        elif stream is not None:
            files = {filename: stream}
        else:
            self.logger.error("path and stream are None")
            return
        post_res = requests.post(post_url, files=files)
        if not post_res.ok:
            self.logger.error(f"upload_file got error: {post_res.status_code} - {post_res.json().get('error')}")
            return None
        post_res = post_res.json()

        res = {
            "url": post_url,
            "fid": fid,
            "filename": post_res.get('name')
        }

        return res

    def get_image(self, fid=None, url=None, pil=True, **kwargs):
        if fid is not None:
            # TODO get fid url
            url = None
        elif url is not None:
            url = url
        data = self.get_file(url, **kwargs)
        if not data:
            return
        out = io.BytesIO(data)
        out.seek(0)
        pil_img = Image.open(out)
        if pil is True:
            return pil_img
        else:
            return np.array(pil_img)

    def get_file(self, url, **kwargs):
        params = '&'.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
        param = "?" + params if params else ""
        url = f"{url}{param}"
        res = requests.get(url)

        if not res.ok:
            self.logger.error(f"get_file got error: {res.status_code}- {res.json().get('error')}")
            return None

        ret = res.content

        return ret

    def delete_file(self, fid=None, url=None):
        if url is not None:
            res = requests.delete(url)
            if not res.ok:
                self.logger.error(f"delete file got error: {res.status_code}- {res.json().get('error')}")
                return False
        return True


if __name__ == '__main__':
    from utils.config import get_config, set_config
    set_config('./configs/config.yaml')
    _cfg = get_config()
    i = SeaWeedFS(cfg=_cfg)

    _ret = i.get_status()
    print(_ret)
    # print(ret['Version'])

    # ret = i.get_volume_status()
    # print(ret)

    # ret = i.get_writable_collection()
    # print(ret)

    # with open('/home/dongle94/Pictures/monkey.jpeg', 'rb') as out:
    #     print(len(out.read()), type(out.read()))
    #     pil = Image.open(out)
    #     pil.save('/home/dongle94/monkey.jpeg')
    _img = '/home/dongle94/Pictures/monkey.jpeg'
    _ret = i.put_image_collection(image=_img, filename=_img)
    print(_ret)
    # _ret = i.put_image(image=_img, filename=_img)
    # print(_ret)
    # _ret = i.put_file(path=_img, filename=_img)
    # print(_ret)

    # ret = i.allocate_collection()
    # print(ret)

    # ret = i.get_status()
    # print(ret)

    # ret = i.get_volume_status()
    # print(ret)