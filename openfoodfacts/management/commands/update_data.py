from django.core.management.base import BaseCommand

from ...models import Category, Product
from .database import Database


class Command(BaseCommand):
    help = 'update data'

    def handle(self, *args, **kwargs):
        print("Updating data...")
        Database.connect()
        substitutes = self.get_substitutes()
        print("Substitutes saved !")
        products = Database.load("openfoodfacts_product")
        for product in products:
            if product[0] not in substitutes:
                Database.delete(product[0])
        print("Products deleted !")
        self.load()
        self.delete_duplicate(substitutes)
        Database.disconnect()


    def get_substitutes(self):
        print("Saving substitutes...")
        substitute_list = list()
        substitutes = Database.load("openfoodfacts_substitute")
        for substitute in substitutes:
            substitute_list.append(substitute[1])
            substitute_list.append(substitute[2])
        return set(substitute_list)


    def load(self):
        print('Insertion des données...')
        Category.load()
        Product.load()
        Product.objects.filter(categories=None).delete()
        print('Données insérées')

    def delete_duplicate(self, substitutes):
        all_duplicated = list()
        duplicated_result = list()
        duplicated_products = Database.get_duplicate_product()
        for elt in duplicated_products:
            duplicated_result.append(
                Database.products_from_off_id(elt[0])
            )
        for elt in duplicated_result:
            all_duplicated.append(elt[0][0])
            all_duplicated.append(elt[1][0])
        for elt in all_duplicated:
            if elt not in substitutes:
                Database.delete(elt)
