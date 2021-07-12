import uuid

import psycopg2.extras


class Database:

    databaseConnection = None

    @staticmethod
    def connect():
        conn = psycopg2.connect(database="pur_beurre",
                                user="django",
                                password="Thomas040417!",
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

    def get_product_from_key(key):
        cur = Database.cursor()
        cur.execute(f"select * from openfoodfacts_product where id = '{key}'")
        return cur.fetchall()

    def delete(product_id):
        cur = Database.cursor()
        cur.execute(f"delete from openfoodfacts_product_categories where product_id = '{product_id}'")
        cur.execute(f"delete from openfoodfacts_product where id = '{product_id}'")
        Database.databaseConnection.commit()

    def get_duplicate_product():
        cur = Database.cursor()
        cur.execute("select off_id, COUNT(off_id) from openfoodfacts_product GROUP BY off_id HAVING COUNT(off_id) > 1")
        return cur.fetchall()

    def products_from_off_id(off_id):
        cur = Database.cursor()
        cur.execute(f"select id, name from openfoodfacts_product WHERE off_id = '{off_id}'")
        return cur.fetchall()