from ...models import Category, Product
from .database import Database


def delete_product_with_no_categories():
    """
    deleting all products with no categories
    """
    Product.objects.filter(categories=None).delete()


def main():
    """
    inserting DATA in DB
    """
    print('Insertion des données...')
    Database.connect()
    Category.load()
    Product.load()
    delete_product_with_no_categories()
    Database.disconnect()
    print('Données insérées')


if __name__ == "__main__":
    main()
