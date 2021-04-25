from django.contrib.auth.models import AbstractUser
from django.db import models

from openfoodfacts.models import Product

# Create your models here.


class CustomUser(AbstractUser):
    substitute = models.ManyToManyField(Product)
