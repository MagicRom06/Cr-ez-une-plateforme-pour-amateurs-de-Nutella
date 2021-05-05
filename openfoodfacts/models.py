import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=200)
    brands = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=10)
    image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    kcal_100g = models.IntegerField()
    off_id = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class Substitute(models.Model):
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
