from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from .models import SubscribedUsers


class HomePageViewTest(TestCase):
    """
    testing home page
    """
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui, mais de qualité !")
        self.assertTemplateUsed(response, 'home_page/home.html')


class NewsletterPageViewTest(TestCase):
    def test_newsletter_page_status_code(self):
        response = self.client.get(reverse('newsletter'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Souscription à notre newsletter')
        # self.assertTemplateUsed(response, 'home_page/newsletter.html')

    def test_newsletter_form_post(self):
        self.client.post(
            reverse(
                'newsletter'),
            {
                "email": "test@test.com",
                "name": "TEST"
            }
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            'Souscription NewsLetter'
        )
        self.assertTrue(
            SubscribedUsers.objects.all().count(), 1)
        self.assertEqual(
            SubscribedUsers.objects.all()[0].email, "test@test.com")
        self.assertEqual(
            SubscribedUsers.objects.all()[0].name, "TEST")


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
        cls.selenium = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chromeOptions
        )
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
