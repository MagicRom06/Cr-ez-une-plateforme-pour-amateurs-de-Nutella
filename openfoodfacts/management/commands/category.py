import json
import ssl
import urllib.request


class Category:
    def __init__(self, name):
        self._name = name

    @staticmethod
    def load():
        categories_list = list()
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        response = urllib.request.urlopen(
            "https://fr.openfoodfacts.org/categories.json/",
            context=scontext)
        data = json.loads(response.read())
        for category in data["tags"]:
            if ":" not in category['name'] and \
               "-" not in category['name'] and \
               category['products'] > 1000:
                cat = Category(category['name'])
                categories_list.append(cat)
        return categories_list

    def display(self):
        print('name: {}'.format(self._name))

    def name(self):
        return self._name
