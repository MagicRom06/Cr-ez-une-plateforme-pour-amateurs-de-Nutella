import json
import ssl
import urllib.request


class Product:
    def __init__(
        self,
        name,
        brands,
        nutriscore,
        image,
        categories,
        nutri_benchmark,
        off_id
    ):
        self._name = name
        self._brands = brands
        self._nutriscore = nutriscore
        self._image = image
        self._categories = categories
        self._nutri_benchmark = nutri_benchmark
        self._off_id = off_id

    @staticmethod
    def load():
        product_list = list()
        i = 1
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        while i <= 50:
            response = urllib.request.urlopen(
                "https://fr.openfoodfacts.org/products.json/?page={}"
                .format(i),
                context=scontext)
            data = json.loads(response.read())
            for elt in data['products']:
                if 'nutriscore_grade' in elt.keys() and \
                   'image_url' in elt.keys() and \
                   'brands' in elt.keys() and \
                   'energy-kcal_100g' in elt['nutriments'].keys() and \
                   isinstance(elt['nutriments']['energy-kcal_100g'], int):
                    product = Product(
                        elt['product_name'],
                        elt['brands'],
                        elt['nutriscore_grade'],
                        elt['image_url'],
                        elt['categories'],
                        elt['nutriments']['energy-kcal_100g'],
                        elt['_id']
                    )
                    product_list.append(product)
            i += 1
        return product_list

    def display(self):
        print(
            """name: {},
             brands: {},
             nutriscore: {},
             image: {},
             categories : {},
             nutri_benchmark: {}""".format(
                self._name,
                self._brands,
                self._nutriscore,
                self._image,
                self._categories,
                self._nutri_benchmark))

    def name(self):
        return self._name

    def brands(self):
        return self._brands

    def nutriscore(self):
        return self._nutriscore

    def image(self):
        return self._image

    def categories(self):
        return self._categories

    def nutri_benchmark(self):
        return self._nutri_benchmark

    def off_id(self):
        return self._off_id
