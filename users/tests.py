from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class CustomUserTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name"
        )

    def test_account_page_view(self):
        """
        testing account page access
        """
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.email)
        self.assertTemplateUsed(response, 'users/account.html')

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            password='test123',
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@test.com',
            password='test123'
        )
        self.assertEqual(admin_user.email, 'admin@test.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_reset_password_page(self):
        response = self.client.get(reverse('account_reset_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset.html')

    def test_reset_password_form_post(self):
        response = self.client.post(
            reverse('account_reset_password'), {'email': 'test@test.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            '[example.com] E-mail de réinitialisation de mot de passe'
            )

    def test_change_password_page(self):
        User = get_user_model()
        User.objects.create_user(
            email='test@email.com',
            password='test12345',
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.client.login(email='test@email.com', password='test12345')
        response = self.client.get(reverse('account_change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_change.html')
        self.assertContains(response, 'Modifier le mot de passe')


class SignupTests(TestCase):
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign up')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.email
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(
            get_user_model().objects.all()[0].email, new_user.email)

    def test_signup_form_post(self):
        mail.outbox = []
        self.client.post(
            reverse('account_signup'),
            {
                'email': 'test@test.com',
                'password1': 'test12345!',
                'password2': 'test12345!',
                'first_name': 'test',
                'last_name': 'test_last_name'
            }
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            '[example.com] Confirmez votre adresse e-mail'
        )

    def test_user_update_page(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            password='test12345',
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.client.login(email='test@email.com', password='test12345')
        response = self.client.get(reverse(
            'user_update',
            kwargs={'pk': user.id})
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_update.html')
        self.assertContains(response, user.email)
        self.assertContains(response, 'Modifier mes informations')

    def test_user_update_post_form(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@email.com',
            password='test12345',
            first_name="test_first_name",
            last_name="test_last_name"
        )
        self.client.login(email='test@email.com', password='test12345')
        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.id}),
            {
                'email': 'test@test.com',
                'first_name': 'test',
                'last_name': 'test_last_name_changed',
            }
        )
        response = self.client.get(reverse(
            'user_update',
            kwargs={'pk': user.id}))
        self.assertContains(response, 'test@test.com')
        self.assertContains(response, 'test')
        self.assertContains(response, 'test_last_name_changed')


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            'test subject', 'test message',
            'notification-pur-beurre@monaco.mc', ['test@example.com'],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test subject')
        self.assertEqual(mail.outbox[0].body, 'test message')
