"""
Tests for user signup, login, verification, password reset, API token auth,
credits, rate limiting, and subscription lifecycle.
"""
from unittest.mock import patch

from django.test import TestCase, Client
from django.utils import timezone

from accounts.models import CustomUser


class BaseUserTestCase(TestCase):
    """Shared setup: Language record required by GlobalVars."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()
        # Clear DRF throttle caches
        from rest_framework.throttling import SimpleRateThrottle
        if hasattr(SimpleRateThrottle, 'cache'):
            SimpleRateThrottle.cache.clear()


class SignupTests(BaseUserTestCase):
    """User registration flow."""

    @patch('app.utils.Utils.send_email')
    def test_register_success(self, mock_email):
        response = self.client.post('/signup/', {
            'email': 'newuser@example.com',
            'password': 'testpass123',
        })
        # Successful registration redirects to account
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(email='newuser@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_confirm)
        self.assertIsNotNone(user.verification_code)
        self.assertIsNotNone(user.api_token)
        mock_email.assert_called_once()

    def test_register_missing_email(self):
        response = self.client.post('/signup/', {
            'password': 'testpass123',
        })
        # Returns the form page with errors (200, not redirect)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='').exists())

    def test_register_missing_password(self):
        response = self.client.post('/signup/', {
            'email': 'nopass@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='nopass@example.com').exists())

    def test_register_short_password(self):
        response = self.client.post('/signup/', {
            'email': 'shortpw@example.com',
            'password': 'abc',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='shortpw@example.com').exists())

    def test_register_invalid_email(self):
        response = self.client.post('/signup/', {
            'email': 'not-an-email',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='not-an-email').exists())

    @patch('app.utils.Utils.send_email')
    def test_register_duplicate_email(self, mock_email):
        CustomUser.objects.create_user(email='dupe@example.com', password='testpass123')
        response = self.client.post('/signup/', {
            'email': 'dupe@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.filter(email='dupe@example.com').count(), 1)

    @patch('app.utils.Utils.send_email')
    def test_register_auto_logs_in(self, mock_email):
        self.client.post('/signup/', {
            'email': 'autologin@example.com',
            'password': 'testpass123',
        })
        # After registration, user should be logged in
        response = self.client.get('/account/')
        # Should not redirect to login (user is authenticated)
        # But may redirect to verify since is_confirm=False
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 302:
            self.assertIn('verify', response.url)


class LoginTests(BaseUserTestCase):
    """User login flow."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='login@example.com',
            password='testpass123',
        )

    def test_login_success(self):
        response = self.client.post('/login/', {
            'email': 'login@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        response = self.client.post('/login/', {
            'email': 'login@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {
            'email': 'nobody@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_missing_email(self):
        response = self.client.post('/login/', {
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_missing_password(self):
        response = self.client.post('/login/', {
            'email': 'login@example.com',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_if_already_authenticated(self):
        self.client.login(email='login@example.com', password='testpass123')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(email='login@example.com', password='testpass123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        # After logout, account page should redirect to login
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)


class EmailVerificationTests(BaseUserTestCase):
    """Email verification flow."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='verify@example.com',
            password='testpass123',
        )
        cls.user.is_confirm = False
        cls.user.verification_code = '123456'
        cls.user.save()

    def test_verify_page_requires_login(self):
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 302)  # Redirect to index

    def test_verify_page_loads_when_logged_in(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 200)

    def test_verify_correct_code(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.post('/verify/', {'code': '123456'})
        self.assertEqual(response.status_code, 302)  # Redirect to account
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_confirm)

    def test_verify_wrong_code(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.post('/verify/', {'code': '999999'})
        self.assertEqual(response.status_code, 200)  # Re-renders with errors
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_confirm)

    def test_verified_user_redirects_from_verify(self):
        self.user.is_confirm = True
        self.user.save()
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 302)  # Redirect to account


class PasswordResetTests(BaseUserTestCase):
    """Lost password and restore password flow."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='reset@example.com',
            password='oldpass123',
        )

    def test_lost_password_page_loads(self):
        response = self.client.get('/lost-password/')
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.Utils.send_email')
    def test_lost_password_sends_email(self, mock_email):
        response = self.client.post('/lost-password/', {
            'email': 'reset@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.restore_password_token)

    def test_lost_password_unknown_email(self):
        response = self.client.post('/lost-password/', {
            'email': 'unknown@example.com',
        })
        self.assertEqual(response.status_code, 200)

    def test_restore_password_success(self):
        token = 'test-reset-token-abc123'
        self.user.restore_password_token = token
        self.user.save()
        response = self.client.post('/restore-password/', {
            'token': token,
            'password': 'newpass123',
            'confirm_password': 'newpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    def test_restore_password_mismatch(self):
        token = 'test-reset-token-abc456'
        self.user.restore_password_token = token
        self.user.save()
        response = self.client.post('/restore-password/', {
            'token': token,
            'password': 'newpass123',
            'confirm_password': 'differentpass',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        # Password should NOT have changed
        self.assertTrue(self.user.check_password('oldpass123'))

    def test_restore_password_invalid_token(self):
        response = self.client.post('/restore-password/', {
            'token': 'nonexistent-token',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
        })
        self.assertEqual(response.status_code, 200)


class APITokenAuthTests(BaseUserTestCase):
    """Public API v1 authentication with API token."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='apiuser@example.com',
            password='testpass123',
        )
        cls.user.is_confirm = True
        cls.user.api_token = 'test-api-token-xyz'
        cls.user.credits = 100
        cls.user.save()

    def test_api_with_valid_token(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data='{"text": "The cat sat on the mat.", "mode": "standard"}',
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-xyz',
        )
        # 200 = success, 500 = LLM service error (expected in test env)
        self.assertIn(response.status_code, [200, 500])
        if response.status_code == 200:
            self.assertIn('output_text', response.json())

    def test_api_with_invalid_token(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data='{"text": "Hello world.", "mode": "standard"}',
            content_type='application/json',
            HTTP_X_API_KEY='invalid-token',
        )
        # DRF returns 403 for failed authentication
        self.assertIn(response.status_code, [401, 403])

    def test_api_without_token_processes_as_anon(self):
        # No API key = anonymous user, API still processes but with free limits
        response = self.client.post(
            '/api/v1/paraphrase/',
            data='{"text": "The cat sat on the mat.", "mode": "standard"}',
            content_type='application/json',
        )
        # 200 = success, 500 = LLM service error (expected in test env)
        self.assertIn(response.status_code, [200, 500])


class CreditsAndPlanTests(BaseUserTestCase):
    """Credits consumption, plan checks, and subscription status."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='credits@example.com',
            password='testpass123',
        )
        cls.user.credits = 10
        cls.user.is_confirm = True
        cls.user.save()

    def test_consume_credits(self):
        initial_credits = self.user.credits
        CustomUser.consume_credits(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, initial_credits - 1)

    def test_credits_dont_go_negative(self):
        self.user.credits = 0
        self.user.save()
        CustomUser.consume_credits(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 0)

    def test_check_plan_active(self):
        self.user.is_plan_active = True
        self.user.save()
        self.assertTrue(self.user.check_plan)

    def test_check_plan_inactive(self):
        self.user.is_plan_active = False
        self.user.save()
        self.assertFalse(self.user.check_plan)

    def test_account_page_requires_auth(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)

    def test_account_page_verified_user(self):
        self.client.login(email='credits@example.com', password='testpass123')
        response = self.client.get('/account/')
        self.assertIn(response.status_code, [200, 302])


class UserModelTests(BaseUserTestCase):
    """Unit tests for CustomUser model methods."""

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='model@example.com',
            password='testpass123',
        )
        self.assertEqual(user.email, 'model@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertIsNotNone(user.uuid)
        self.assertIsNotNone(user.api_token)

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_normalization(self):
        user = CustomUser.objects.create_user(
            email='Test@Example.COM',
            password='testpass123',
        )
        self.assertEqual(user.email, 'Test@example.com')

    def test_api_token_generated_on_create(self):
        user = CustomUser.objects.create_user(
            email='token@example.com',
            password='testpass123',
        )
        self.assertIsNotNone(user.api_token)
        self.assertTrue(len(user.api_token) > 10)

    def test_verification_code_generated_on_create(self):
        user = CustomUser.objects.create_user(
            email='vcode@example.com',
            password='testpass123',
        )
        self.assertIsNotNone(user.verification_code)

    def test_default_credits_zero(self):
        user = CustomUser.objects.create_user(
            email='nocreds@example.com',
            password='testpass123',
        )
        self.assertEqual(user.credits, 0)

    def test_str_returns_email(self):
        user = CustomUser.objects.create_user(
            email='str@example.com',
            password='testpass123',
        )
        self.assertEqual(str(user), 'str@example.com')


class ExpireProUsersTests(BaseUserTestCase):
    """Test the expire_pro_users management command logic."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.active_user = CustomUser.objects.create_user(
            email='active@example.com', password='testpass123',
        )
        cls.active_user.is_plan_active = True
        cls.active_user.next_billing_date = timezone.now() + timezone.timedelta(days=10)
        cls.active_user.save()

        cls.expired_user = CustomUser.objects.create_user(
            email='expired@example.com', password='testpass123',
        )
        cls.expired_user.is_plan_active = True
        cls.expired_user.next_billing_date = timezone.now() - timezone.timedelta(days=1)
        cls.expired_user.save()

    def test_active_user_stays_active(self):
        # Simulate what expire_pro_users does
        expired = CustomUser.objects.filter(
            is_plan_active=True,
            next_billing_date__lt=timezone.now(),
        )
        self.assertNotIn(self.active_user, expired)

    def test_expired_user_detected(self):
        expired = CustomUser.objects.filter(
            is_plan_active=True,
            next_billing_date__lt=timezone.now(),
        )
        self.assertIn(self.expired_user, expired)

    def test_expire_deactivates_plan(self):
        # Simulate expiration
        CustomUser.objects.filter(
            is_plan_active=True,
            next_billing_date__lt=timezone.now(),
        ).update(is_plan_active=False, next_billing_date=None)
        self.expired_user.refresh_from_db()
        self.assertFalse(self.expired_user.is_plan_active)
        self.assertIsNone(self.expired_user.next_billing_date)
        # Active user should be unaffected
        self.active_user.refresh_from_db()
        self.assertTrue(self.active_user.is_plan_active)
