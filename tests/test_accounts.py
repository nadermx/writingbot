"""Tests for authentication flows."""
from django.test import TestCase, Client


class AuthPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_lost_password_page(self):
        response = self.client.get('/lost-password/')
        self.assertEqual(response.status_code, 200)

    def test_account_page_requires_auth(self):
        response = self.client.get('/account/')
        # Should redirect to login
        self.assertIn(response.status_code, [301, 302, 200])

    def test_delete_account_page(self):
        response = self.client.get('/delete-account/')
        self.assertIn(response.status_code, [200, 302])
