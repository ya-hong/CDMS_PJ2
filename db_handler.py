# 用于连接数据库

import psycopg2
from configparser import ConfigParser


class DB_handler:
    def __init__(self):
        self.section = "postgresql"
        self.config_path = "../sql/database.ini"
        self.init_tables()

    def init_tables(self):
        commands = (
            "CREATE TABLE USERS ( \
            UID VARCHAR(255) PRIMARY KEY, \
            PWD TEXT NOT NULL, \
            SHOP_ID VARCHAR(255) NOT NULL, \
            BALANCE FLOAT NOT NULL\
            )\
            ",
            " CREATE TABLE SHOPS ( \
            SHOP_ID VARCHAR(255) PRIMARY KEY, \
            UID VARCHAR(255) NOT NULL, \
            RANKING INTEGER\
            )\
            ",
            " CREATE TABLE BOOKS ( \
            BOOK_ID VARCHAR(255) PRIMARY KEY, \
            UID VARCHAR(255) NOT NULL, \
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
            )\
            ",
            " CREATE TABLE ORDERS (\
            ORDER_ID VARCHAR(255) PRIMARY KEY,\
            UID VARCHAR(255) NOT NULL,\
            SHOP_ID VARCHAR(255) NOT NULL, \
            BOOK_ID VARCHAR(255) NOT NULL,\
            ORDER_TIME TEXT NOT NULL, \
            ORDER_QUANTITY INTEGER NOT NULL,\
            CURRENT_STATE INTEGER NOT NULL\
            )\
            ",
            "ALTER TABLE USERS \
            ADD FOREIGN KEY (SHOP_ID) \
            REFERENCES SHOPS(SHOP_ID) \
            ",
            "ALTER TABLE SHOPS \
            ADD FOREIGN KEY (UID) \
            REFERENCES USERS(UID) \
            ",
            "ALTER TABLE BOOKS\
            ADD FOREIGN KEY (UID)\
            REFERENCES USERS(UID),\
            ADD FOREIGN KEY (SHOP_ID)\
            REFERENCES SHOPS(SHOP_ID)\
            ",
            "ALTER TABLE ORDERS\
            ADD FOREIGN KEY (UID)\
            REFERENCES USERS(UID),\
            ADD FOREIGN KEY (SHOP_ID)\
            REFERENCES SHOPS(SHOP_ID),\
            ADD FOREIGN KEY (BOOK_ID)\
            REFERENCES BOOKS(BOOK_ID)\
            "
        )
        try:
            conn = self.db_connect()
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close
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
