import logging

import mysql.connector


class DBManager(object):
    def __init__(self, user, password, host='localhost', database='ANNODATA', logger: logging.Logger = None):

        con = mysql.connector.connect(user=user,
                                      password=password,
                                      host=host)
        cur = con.cursor()
        sql = open('./core/init.sql').read()
        cur.execute(sql)
        con.close()
        self.con = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
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
        data = tuple(name)

        cursor = self.con.cursor()
        cursor.execute(sql, data)
        ret = cursor.fetchall()
        cursor.close()

        return ret


if __name__ == "__main__":
    import time
    from utils.config import set_config, get_config

    set_config('./configs/config.yaml')
    cfg = get_config()

    db = DBManager(user=cfg.user, password=cfg.password, host=cfg.host, database=cfg.database)

    time.sleep(0.1)
    db.show_tables()
