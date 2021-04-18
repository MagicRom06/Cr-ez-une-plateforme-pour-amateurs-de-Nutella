from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'brands', 'image', 'nutriscore', 'kcal_100g')


admin.site.register(Product, ProductAdmin)
