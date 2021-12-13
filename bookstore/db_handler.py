# 用于连接数据库

import psycopg2
from configparser import ConfigParser
import os


class DB_handler:
    def __init__(self):
        self.section = "postgresql"
        print(os.getcwd())
        self.config_path = "./database.ini"
        self.init_tables()

    def init_tables(self):
        conn = None
        try:
            conn = self.db_connect()
            cur = conn.cursor()
            with open(os.path.join(os.path.dirname(__file__), 'create_table.sql'), 'r') as f:
                cur.execute(f.read())
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
            print('Database connection closed.')

    def config(self):
        parser = ConfigParser()
        parser.read(self.config_path)

        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception("Section {0} not found in the {1} file".format(self.section, self.config_path))

        return db

    def db_connect(self):
        conn = None
        try:
            params = self.config()

            conn = psycopg2.connect(**params)
            print("Successfully connected.")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to connect.")
            print(error)

        return conn


db_handler = DB_handler()
