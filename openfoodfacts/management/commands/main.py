from .category import Category
from .database import Database
from .product import Product


def insert_cat():
    categories = Category.load()
    for category in categories:
        Database.insert_category(category.name())


def insert_product():
    products = Product.load()
    for product in products:
        Database.insert_products(
            product.name(),
            product.brands(),
            product.nutriscore(),
            product.image(),
            product.nutri_benchmark(),
            product.off_id())


def insert_products_categories():
    key = list()
    categories_from_db = Database.load("pages_category")
    products_from_db = Database.load("pages_product")
    product_from_api = Product.load()
    for product in products_from_db:
        for api_product in product_from_api:
            if product[1] == api_product.name():
                for category in api_product.categories().split(', '):
                    for category_db in categories_from_db:
                        if category == category_db[1]:
                            key.append((product[0], category_db[0]))
    new_key = list(dict.fromkeys(key))
    for elt in new_key:
        Database.insert_products_categories(elt[0], elt[1])


def main():
    print('Insertion des données...')
    Database.connect()
    insert_cat()
    insert_product()
    insert_products_categories()
    Database.disconnect()


if __name__ == "__main__":
    main()
