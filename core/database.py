import time
import logging

import mysql.connector


class DBManager(object):
    def __init__(self, user, password, host='localhost', port=3306, database='ANNODATA', logger: logging.Logger = None):

        con = mysql.connector.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port)
        cur = con.cursor()
        sql = open('./core/init.sql').read()
        cur.execute(sql)
        con.close()
        time.sleep(1)
        self.con = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        self.logger = logger
        if self.logger is not None:
            self.logger.info("Initializing database")

    def get_cursor(self):
        try:
            cursor = self.con.cursor()
        except mysql.connector.Error as err:
            self.con.reconnect()
            cursor = self.con.cursor()
        return cursor

    def show_tables(self):
        with self.con.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
        for r in rows:
            print(r)

    def create_dataset(self, name, data_type, dsec=""):
        sql = "INSERT INTO dataset (name, data_type, data_desc) VALUES (%s, %s, %s)"
        data = (name, data_type, dsec)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Dataset '%s' created", name)
        return cursor.lastrowid

    def read_dataset(self):
        sql = "SELECT * FROM dataset"

        cursor = self.get_cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def read_dataset_by_name(self, name):
        sql = "SELECT * FROM dataset WHERE name = (%s)"
        data = (name, )

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def delete_dataset_by_name(self, name):
        sql = "DELETE FROM dataset WHERE name = (%s)"
        data = (name, )

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Dataset '%s' is deleted.", name)

    def create_image_data(self, dataset_id, filename, image_fid, image_url, width, height):
        sql = ("INSERT INTO image_data (dataset_id, filename, image_fid, image_url, width, height) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (dataset_id, filename, image_fid, image_url, width, height)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Image '%s' inserted", filename)
        return cursor.lastrowid

    def read_image_data_by_dataset_id(self, dataset_id):
        sql = "SELECT * FROM image_data WHERE dataset_id = (%s)"
        data = (dataset_id,)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def read_image_data_by_image_data_id(self, image_data_id):
        sql = "SELECT * FROM image_data WHERE image_data_id = (%s)"
        data = (image_data_id,)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def delete_image_data_by_image_id(self, image_id):
        sql = "DELETE FROM image_data WHERE image_data_id = (%s)"
        data = (image_id,)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Image '%s' is deleted.", image_id)

    def create_label_field(self, name, dataset_id, label_format, label_type, is_duplicate, detail):
        sql = ("INSERT INTO label_field (name, dataset_id, subject, type, duplicatable, detail) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (name, dataset_id, label_format, label_type, is_duplicate, detail)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Label_field '%s-%s' created", label_format, label_type)
        return cursor.lastrowid

    def read_label_field_by_dataset_id(self, dataset_id):
        sql = "SELECT * FROM label_field WHERE dataset_id = (%s)"
        data = (dataset_id,)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def update_label_field(self, where=None, **kwargs):
        sql = "UPDATE label_field SET"
        data = []
        if kwargs:
            for key, value in kwargs.items():
                sql += f' {key} = (%s)' if sql[-3:] == "SET" else f' AND {key} = (%s)'
                data.append(value)

        if where is not None:
            sql += " WHERE"
            for key, value in where.items():
                sql += f' {key} = (%s)' if sql[-5:] == "WHERE" else f' AND {key} = (%s)'
                data.append(value)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()
        self.logger.debug(f"Update label_data: {sql}, {data}")

    def delete_label_field_by_label_field_id(self, label_field_id):
        sql = "DELETE FROM label_field WHERE label_field_id = (%s)"
        data = (label_field_id,)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("label_field_id '%s' is deleted.", label_field_id)

    def create_label_data(self, image_data_id, label_field_id, ref_box_id=None,
                          is_box=0, coord=None, cls=None, caption=None):
        sql = ("INSERT INTO label_data "
               "(image_data_id, label_field_id, ref_box_id, is_box, coord, cls, caption) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        data = (image_data_id, label_field_id, ref_box_id, is_box, coord, cls, caption)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        log_text = f"Create label_data - image_idx: {image_data_id}, label_field_idx: {label_field_id}"
        if is_box:
            log_text += f", ref_box_id: {ref_box_id}"
        if coord:
            log_text += f", coord: {coord}"
        if cls:
            log_text += f", class: {cls}"
        if caption:
            log_text += f", caption: {caption}"
        self.logger.info(log_text)
        return cursor.lastrowid

    def read_label_data(self, **kwargs):
        sql = "SELECT * FROM label_data"
        data = []
        if kwargs:
            sql += " WHERE"
            for key, value in kwargs.items():
                sql += f' {key} = (%s)' if sql[-5:] == "WHERE" else f' AND {key} = (%s)'
                data.append(value)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()
        self.logger.debug(f"Read label_data: {sql}, {data}")

        return ret

    def delete_label_data(self, **kwargs):
        sql = "DELETE FROM label_data"
        data = []
        if kwargs:
            sql += " WHERE"
            for key, value in kwargs.items():
                sql += f' {key} = (%s)' if sql[-5:] == "WHERE" else f' AND {key} = (%s)'
                data.append(value)

        cursor = self.get_cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()
        self.logger.debug(f"Delete label_data: {sql}, {data}")


if __name__ == "__main__":
    import os
    import sys

    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    if ROOT_PATH not in sys.path:
        sys.path.append(ROOT_PATH)
    from utils.config import set_config, get_config

    set_config('./configs/config.yaml')
    cfg = get_config()

    db = DBManager(user=cfg.user, password=cfg.password, host=cfg.host, database=cfg.database)

    time.sleep(0.1)
    db.show_tables()

    # ret = db.read_dataset_by_name('sample1')
    # print(ret)
