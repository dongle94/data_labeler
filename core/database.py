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

    def show_tables(self):
        with self.con.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
        for r in rows:
            print(r)

    def create_dataset(self, name, data_type, dsec=""):
        sql = "INSERT INTO dataset (name, data_type, data_desc) VALUES (%s, %s, %s)"
        data = (name, data_type, dsec)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Dataset '%s' created", name)

    def read_dataset(self):
        sql = "SELECT * FROM dataset"

        cursor = self.con.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def read_dataset_detail(self, name):
        sql = "SELECT * FROM dataset WHERE name = (%s)"
        data = (name, )

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def delete_dataset(self, name):
        sql = "DELETE FROM dataset WHERE name = (%s)"
        data = (name, )

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Dataset '%s' is deleted.", name)

    def insert_image(self, dataset_id, filename, image_url, width, height):
        sql = ("INSERT INTO image_data (dataset_id, filename, image_url, width, height) "
               "VALUES (%s, %s, %s, %s, %s)")
        data = (dataset_id, filename, image_url, width, height)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Image '%s' inserted", filename)
        return cursor.lastrowid

    def read_image_by_dataset_id(self, dataset_id):
        sql = "SELECT * FROM image_data WHERE dataset_id = (%s)"
        data = (dataset_id,)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret

    def delete_image_by_image_id(self, image_id):
        sql = "DELETE FROM image_data WHERE image_data_id = (%s)"
        data = (image_id,)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Image '%s' is deleted.", image_id)

    def create_label_field(self, name, dataset_id, label_format, label_type, is_duplicate, detail):
        sql = ("INSERT INTO label_field (name, dataset_id, subject, type, duplicatable, detail) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (name, dataset_id, label_format, label_type, is_duplicate, detail)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        self.con.commit()
        cursor.close()

        self.logger.info("Label_field '%s-%s' created", label_format, label_type)
        return cursor.lastrowid

    def read_label_field_by_dataset_id(self, dataset_id):
        sql = "SELECT * FROM label_field WHERE dataset_id = (%s)"
        data = (dataset_id,)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret


if __name__ == "__main__":
    import time
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

    # ret = db.read_dataset_detail('sample1')
    # print(ret)
