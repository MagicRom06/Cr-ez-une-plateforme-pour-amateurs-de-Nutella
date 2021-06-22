from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class HomePageViewTest(TestCase):
    """
    testing home page
    """
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui, mais de qualité !")
        self.assertTemplateUsed(response, 'home_page/home.html')
