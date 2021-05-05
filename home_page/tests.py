from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class HomePageViewTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui, mais de qualité !")
        self.assertTemplateUsed(response, 'home_page/home.html')


class SearchFormTest(LiveServerTestCase):
    def test_search_form(self):
        selenium = webdriver.Chrome(ChromeDriverManager().install())
        selenium.get('http://127.0.0.1:8000/')
        search = selenium.find_element_by_id('search')
        submit = selenium.find_element_by_id('submit_button')
        search.send_keys('nutella')
        submit.send_keys(Keys.RETURN)
        assert 'Resultats' in selenium.page_source
        assert 'Nutella' in selenium.page_source
