# 用于连接数据库

import psycopg2
from configparser import ConfigParser
import os


class DB_handler:
    def __init__(self):
        self.section = "postgresql"
        # 请把 database.ini 移到本文件的相同目录
        self.config_path = os.path.join(os.path.dirname(__file__), 'database.ini')
        self.init_tables()

    def init_tables(self):
        commands = (
            "CREATE TABLE IF NOT EXISTS USERS ( \
            UID VARCHAR(255) PRIMARY KEY, \
            PWD TEXT NOT NULL, \
            BALANCE FLOAT NOT NULL, \
            TOKEN TEXT, \
            TERMINAL TEXT \
            );\
            ",
            " CREATE TABLE IF NOT EXISTS SHOPS ( \
            SHOP_ID VARCHAR(255) PRIMARY KEY, \
            UID VARCHAR(255) NOT NULL, \
            RANKING INTEGER\
            );\
            ",
            " CREATE TABLE IF NOT EXISTS BOOKS ( \
            BOOK_ID TEXT PRIMARY KEY, \
            SHOP_ID VARCHAR(255) NOT NULL, \
            QUANTITY INTEGER NOT NULL, \
            title TEXT, \
            author TEXT, \
            publisher TEXT, \
            original_title TEXT, \
            translator TEXT, \
            pub_year TEXT, \
            pages INTEGER, \
            price INTEGER, \
            currency_unit TEXT, \
            binding TEXT, \
            isbn TEXT, \
            author_intro TEXT, \
            book_intro TEXT, \
            content TEXT, \
            tags TEXT\
            );\
            ",
            " CREATE TABLE IF NOT EXISTS ORDERS (\
            ORDER_ID TEXT PRIMARY KEY, \
            UID VARCHAR(255) NOT NULL,\
            SHOP_ID VARCHAR(255) NOT NULL, \
            ORDER_TIME TEXT NOT NULL, \
            CURRENT_STATE INTEGER NOT NULL\
            );\
            ",
            " CREATE TABLE IF NOT EXISTS ORDER_BOOK (\
            ORDER_ID TEXT, \
            BOOK_ID TEXT NOT NULL,\
            PRIMARY KEY (ORDER_ID, BOOK_ID),\
            FOREIGN KEY (ORDER_ID)\
            REFERENCES ORDERS (ORDER_ID)\
            ON UPDATE CASCADE ON DELETE CASCADE,\
            FOREIGN KEY (BOOK_ID)\
            REFERENCES BOOKS (BOOK_ID)\
            ON UPDATE CASCADE ON DELETE CASCADE,\
            ORDER_QUANTITY INTEGER NOT NULL\
            );\
            "
        )
        fk_commands = (
                       "ALTER TABLE SHOPS \
                        ADD FOREIGN KEY (UID) \
                        REFERENCES USERS(UID); \
                        ",
                       "ALTER TABLE BOOKS\
                        ADD FOREIGN KEY (SHOP_ID)\
                        REFERENCES SHOPS(SHOP_ID);\
                        ",
                       "ALTER TABLE ORDERS\
                        ADD FOREIGN KEY (UID)\
                        REFERENCES USERS(UID),\
                        ADD FOREIGN KEY (SHOP_ID)\
                        REFERENCES SHOPS(SHOP_ID);\
                        ")
        try:
            conn = self.db_connect()
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.execute("SELECT\
                        tc.constraint_name, tc.table_name, kcu.column_name, \
                        ccu.table_name AS foreign_table_name,\
                        ccu.column_name AS foreign_column_name \
                        FROM \
                        information_schema.table_constraints AS tc \
                        JOIN information_schema.key_column_usage AS kcu\
                        ON tc.constraint_name = kcu.constraint_name\
                        JOIN information_schema.constraint_column_usage AS ccu\
                        ON ccu.constraint_name = tc.constraint_name\
                        WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='users' ")
            if cur.rowcount == 0:
                for command in fk_commands:
                    cur.execute(command)
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
