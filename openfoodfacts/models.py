from django.db import models
import uuid
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
