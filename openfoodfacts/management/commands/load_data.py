from django.core.management.base import BaseCommand

from ...models import Category, Product
from .database import Database


class Command(BaseCommand):
    help = 'load data'

    def handle(self, *args, **kwargs):
        """
        inserting DATA in DB
        """
        self.load()

    def delete_product_with_no_categories(self):
        """
        deleting all products with no categories
        """
        Product.objects.filter(categories=None).delete()

    def load(self):
        print('Insertion des données...')
        Database.connect()
        Category.load()
        Product.load()
        self.delete_product_with_no_categories()
        Database.disconnect()
        print('Données insérées')
