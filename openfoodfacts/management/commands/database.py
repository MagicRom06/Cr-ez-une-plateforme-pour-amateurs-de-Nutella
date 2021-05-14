import uuid

import psycopg2.extras


class Database:

    databaseConnection = None

    @staticmethod
    def connect():
        conn = psycopg2.connect(database="pur_beurre",
                                user="django",
                                password="thomas",
                                host="127.0.0.1",
                                port="5432")
        Database.databaseConnection = conn

    @staticmethod
    def cursor():
        return Database.databaseConnection.cursor()

    @staticmethod
    def disconnect():
        Database.databaseConnection.close()
        databaseConnection = None
        return databaseConnection

    @staticmethod
    def insert_category(name):
        cur = Database.cursor()
        sql = """INSERT INTO openfoodfacts_category (name) VALUES (%s);"""
        cur.execute(sql, (name, ))
        Database.databaseConnection.commit()

    @staticmethod
    def insert_products(
        name,
        brands,
        nutriscore,
        image,
        kcal_100g,
        off_id
    ):
        cur = Database.cursor()
        sql = """INSERT INTO openfoodfacts_product (
        id, name, brands, nutriscore, image, kcal_100g, off_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        val = (
            str(uuid.uuid4()),
            name,
            brands,
            nutriscore,
            image,
            kcal_100g,
            off_id,
        )
        cur.execute(sql, val)
        Database.databaseConnection.commit()

    @staticmethod
    def insert_products_categories(product_id, category_id):
        cur = Database.cursor()
        sql = """INSERT INTO openfoodfacts_product_categories (
        product_id, category_id)
        VALUES (%s, %s);"""
        val = (product_id, category_id, )
        cur.execute(sql, val)
        Database.databaseConnection.commit()

    @staticmethod
    def load(table):
        cur = Database.cursor()
        cur.execute("select * from {};".format(table))
        return cur.fetchall()
