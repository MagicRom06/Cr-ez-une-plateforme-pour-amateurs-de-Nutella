from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


class HomePageViewTest(TestCase):
    """
    testing home page
    """
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui, mais de qualité !")
        self.assertTemplateUsed(response, 'home_page/home.html')


class SearchFormTest(StaticLiveServerTestCase):
    """
    live testing search form from home page
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chromeOptions = webdriver.ChromeOptions() 
        chromeOptions.add_experimental_option(
            "prefs", 
            {"profile.managed_default_content_settings.images": 2}
        ) 
        chromeOptions.add_argument("--no-sandbox") 
        chromeOptions.add_argument("--disable-setuid-sandbox") 
        chromeOptions.add_argument("--remote-debugging-port=9222")
        chromeOptions.add_argument("--disable-dev-shm-using") 
        chromeOptions.add_argument("--disable-extensions") 
        chromeOptions.add_argument("--disable-gpu") 
        chromeOptions.add_argument("start-maximized") 
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_search_form(self):
        self.selenium.get(self.live_server_url)
        search = self.selenium.find_element_by_id('search')
        submit = self.selenium.find_element_by_id('submit_button')
        search.send_keys('nutella')
        submit.send_keys(Keys.RETURN)
        assert 'Resultats' in self.selenium.page_source
