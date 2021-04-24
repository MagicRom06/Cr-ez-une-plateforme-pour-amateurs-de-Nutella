from django.test import TestCase
from .models import Product, Category
from django.urls import reverse

# Create your tests here.


class PagesTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='test name',
            brands='test brands',
            nutriscore='a',
            image='test image',
            kcal_100g=100
        )
        self.product.categories.add(
            Category.objects.create(name="test category"))

    def test_product_listing(self):
        self.assertEqual(f'{self.product.name}', 'test name')
        self.assertEqual(f'{self.product.brands}', 'test brands')
        self.assertEqual(f'{self.product.nutriscore}', 'a')
        self.assertEqual(f'{self.product.image}', 'test image')
        self.assertEqual(f'{self.product.kcal_100g}', '100')

    def test_product_search_list_view(self):
        response = self.client.get(
            reverse('search_results'),
            {'search': self.product.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test name')
        self.assertTemplateUsed(response, 'openfoodfacts/search_results.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test name')
        self.assertTemplateUsed(response, 'openfoodfacts/product_detail.html')
