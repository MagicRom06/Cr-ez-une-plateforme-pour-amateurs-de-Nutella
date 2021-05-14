import json
import ssl
import urllib.request
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    """
    model used to manage product's categories
    """
    name = models.CharField(max_length=255)

    @staticmethod
    def load():
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        response = urllib.request.urlopen(
            "https://fr.openfoodfacts.org/categories.json/",
            context=scontext)
        data = json.loads(response.read())
        for category in data["tags"]:
            if ":" not in category['name'] and \
               "-" not in category['name'] and \
               category['products'] > 1000:
                q = Category(name=category['name'])
                q.save()


class Product(models.Model):
    """
    class used to manage products
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    brands = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    kcal_100g = models.IntegerField()
    off_id = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    @staticmethod
    def load():
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
                    q = Product(
                        name=elt['product_name'],
                        brands=elt['brands'],
                        nutriscore=elt['nutriscore_grade'],
                        image=elt['image_url'],
                        kcal_100g=elt['nutriments']['energy-kcal_100g'],
                        off_id=elt['_id']
                    )
                    q.save()
                    for elt in elt['categories'].split(', '):
                        cat = Category.objects.filter(name=elt)
                        if len(cat) > 0:
                            q.categories.add(cat[0])
            i += 1


class Substitute(models.Model):
    """
    model used to manage substitute
    """
    substitute = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="substitute")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user")
