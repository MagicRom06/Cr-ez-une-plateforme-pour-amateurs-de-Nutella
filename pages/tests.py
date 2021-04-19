from django.test import TestCase, client
from .models import Product, Category
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class PagesTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            email = 'test@test.com',
            password='testpass123',
            first_name='test first_name',
            last_name='test last_name'
        )
        self.product = Product.objects.create(
            name = 'test name',
            brands='test brands',
            nutriscore='a',
            image='test image',
            kcal_100g=100
        )
        self.product.categories.add(Category.objects.create(name="test category"))

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui, mais de qualité !")
        self.assertTemplateUsed(response, 'home.html')

    def test_product_listing(self):
        self.assertEqual(f'{self.product.name}', 'test name')
        self.assertEqual(f'{self.product.brands}', 'test brands')
        self.assertEqual(f'{self.product.nutriscore}', 'a')
        self.assertEqual(f'{self.product.image}', 'test image')
        self.assertEqual(f'{self.product.kcal_100g}', '100')

    def test_product_search_list_view(self):
        response = self.client.get(reverse('search_results'), {'search': self.product.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test name')
        self.assertTemplateUsed(response, 'search_results.html')
    
    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test name')
        self.assertTemplateUsed(response, 'product_detail.html')
    
    def test_account_page_view(self):
        self.client.login(username='test', password='testpass123')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.email)
        self.assertTemplateUsed(response, 'account.html')
