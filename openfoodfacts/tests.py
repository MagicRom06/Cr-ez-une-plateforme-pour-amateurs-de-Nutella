from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product

# Create your tests here.


class OpenFoodFactsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@test.com',
            password='testpass123',
            first_name='test first_name',
            last_name='test last_name'
        )
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
        self.assertTemplateUsed(
            response, 'openfoodfacts/search_results.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test name')
        self.assertTemplateUsed(
            response, 'openfoodfacts/product_detail.html')

    def test_save_substitute_without_logged_user(self):
        response = self.client.get(
            reverse('save_substitute', args=(
                self.product.pk, )))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '{}'.format(
                reverse('account_login') + '?next=' + reverse(
                    'save_substitute', args=(self.product.pk, ))))

    def test_save_substitute_with_logged_user(self):
        self.client.login(username='test_user', password='testpass123')
        response = self.client.get(
            reverse('save_substitute', args=(self.product.pk, )))
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(
        # get_user_model().objects.all()
        # [0].substitute.name, self.product.name)
        self.assertRedirects(response, reverse('home'))
