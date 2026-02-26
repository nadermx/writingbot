"""
Comprehensive tests for the accounts app.

Tests cover:
- User model creation (regular and superuser)
- Registration flow (success, validation errors, duplicates)
- Login/logout flows
- Email verification
- Password reset (lost password + restore password)
- Password update (change password while logged in)
- Email normalization and API token generation
- Credits consumption and plan management
- Cancel subscription
- Account deletion
- Resend verification email
"""
from unittest.mock import patch

from django.test import TestCase, Client
from django.utils import timezone

from accounts.models import CustomUser, EmailAddress, AccountType


class BaseAccountTestCase(TestCase):
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
        from rest_framework.throttling import SimpleRateThrottle
        if hasattr(SimpleRateThrottle, 'cache'):
            SimpleRateThrottle.cache.clear()


# ======================================================================
# Model-level tests
# ======================================================================

class CustomUserModelTests(BaseAccountTestCase):
    """Unit tests for the CustomUser model."""

    def test_create_user_basic(self):
        user = CustomUser.objects.create_user(
            email='basic@example.com', password='testpass123'
        )
        self.assertEqual(user.email, 'basic@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_confirm)

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='testpass123')

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            email='admin@example.com', password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_must_be_staff(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='bad@example.com', password='pass', is_staff=False
            )

    def test_create_superuser_must_be_superuser(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='bad2@example.com', password='pass', is_superuser=False
            )

    def test_email_normalization(self):
        user = CustomUser.objects.create_user(
            email='Test@EXAMPLE.COM', password='testpass123'
        )
        # Django's normalize_email lowercases the domain part
        self.assertEqual(user.email, 'Test@example.com')

    def test_uuid_auto_generated(self):
        user = CustomUser.objects.create_user(
            email='uuid@example.com', password='testpass123'
        )
        self.assertIsNotNone(user.uuid)
        self.assertTrue(len(user.uuid) > 10)

    def test_api_token_auto_generated(self):
        user = CustomUser.objects.create_user(
            email='token@example.com', password='testpass123'
        )
        self.assertIsNotNone(user.api_token)
        self.assertTrue(len(user.api_token) > 10)

    def test_verification_code_auto_generated(self):
        user = CustomUser.objects.create_user(
            email='vcode@example.com', password='testpass123'
        )
        self.assertIsNotNone(user.verification_code)
        self.assertEqual(len(user.verification_code), 6)
        self.assertTrue(user.verification_code.isdigit())

    def test_default_credits_zero(self):
        user = CustomUser.objects.create_user(
            email='nocreds@example.com', password='testpass123'
        )
        self.assertEqual(user.credits, 0)

    def test_default_plan_inactive(self):
        user = CustomUser.objects.create_user(
            email='noplan@example.com', password='testpass123'
        )
        self.assertFalse(user.is_plan_active)
        self.assertIsNone(user.plan_subscribed)

    def test_str_returns_email(self):
        user = CustomUser.objects.create_user(
            email='str@example.com', password='testpass123'
        )
        self.assertEqual(str(user), 'str@example.com')

    def test_check_plan_property_active(self):
        user = CustomUser.objects.create_user(
            email='planactive@example.com', password='testpass123'
        )
        user.is_plan_active = True
        user.save()
        self.assertTrue(user.check_plan)

    def test_check_plan_property_inactive(self):
        user = CustomUser.objects.create_user(
            email='planinactive@example.com', password='testpass123'
        )
        user.is_plan_active = False
        user.save()
        self.assertFalse(user.check_plan)


class CreditsTests(BaseAccountTestCase):
    """Tests for credit consumption logic."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='credits@example.com', password='testpass123'
        )
        cls.user.credits = 10
        cls.user.save()

    def test_consume_credits_decrements(self):
        self.user.credits = 10
        self.user.save()
        CustomUser.consume_credits(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 9)

    def test_consume_credits_does_not_go_negative(self):
        self.user.credits = 0
        self.user.save()
        CustomUser.consume_credits(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 0)

    def test_consume_credits_none_user(self):
        # Should not raise, just return None
        result = CustomUser.consume_credits(user=None)
        self.assertIsNone(result)

    def test_consume_credits_from_one(self):
        self.user.credits = 1
        self.user.save()
        CustomUser.consume_credits(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 0)


class CancelSubscriptionTests(BaseAccountTestCase):
    """Tests for subscription cancellation."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='cancel@example.com', password='testpass123'
        )
        cls.user.is_plan_active = True
        cls.user.card_nonce = 'card_nonce_123'
        cls.user.payment_nonce = 'payment_nonce_123'
        cls.user.processor = 'stripe'
        cls.user.next_billing_date = timezone.now() + timezone.timedelta(days=30)
        cls.user.save()

    def test_cancel_subscription_clears_fields(self):
        account, msg = CustomUser.cancel_subscription(self.user)
        self.assertIsNotNone(account)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.card_nonce)
        self.assertIsNone(self.user.payment_nonce)
        self.assertIsNone(self.user.processor)
        self.assertIsNone(self.user.next_billing_date)
        self.assertFalse(self.user.is_plan_active)


class AccountTypeTests(BaseAccountTestCase):
    """Tests for AccountType model."""

    def test_create_account_type(self):
        at = AccountType.objects.create(name='Premium Plan')
        self.assertEqual(at.code_name, 'premium_plan')
        self.assertEqual(str(at), 'Premium Plan')

    def test_code_name_auto_generated(self):
        at = AccountType.objects.create(name='Free Trial Account')
        self.assertEqual(at.code_name, 'free_trial_account')


class EmailAddressTests(BaseAccountTestCase):
    """Tests for EmailAddress model."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='emailtest@example.com', password='testpass123'
        )

    def test_register_email_success(self):
        # Simulate authenticated user
        self.client.force_login(self.user)
        email_obj, msg = EmailAddress.register_email(
            self.user, {'email': 'secondary@example.com'},
            settings={'i18n': {}}
        )
        self.assertIsNotNone(email_obj)
        self.assertEqual(email_obj.email, 'secondary@example.com')

    def test_register_email_missing(self):
        email_obj, msg = EmailAddress.register_email(
            self.user, {'email': ''},
            settings={'i18n': {}}
        )
        self.assertIsNone(email_obj)

    def test_register_email_invalid(self):
        email_obj, msg = EmailAddress.register_email(
            self.user, {'email': 'not-valid'},
            settings={'i18n': {}}
        )
        self.assertIsNone(email_obj)

    def test_register_email_duplicate(self):
        EmailAddress.objects.create(account=self.user, email='dupe@example.com')
        email_obj, msg = EmailAddress.register_email(
            self.user, {'email': 'dupe@example.com'},
            settings={'i18n': {}}
        )
        self.assertIsNone(email_obj)

    def test_str_returns_email(self):
        ea = EmailAddress.objects.create(account=self.user, email='str@example.com')
        self.assertEqual(str(ea), 'str@example.com')

    def test_get_emails(self):
        EmailAddress.objects.create(account=self.user, email='one@example.com')
        EmailAddress.objects.create(account=self.user, email='two@example.com')
        emails = self.user.get_emails()
        self.assertEqual(emails.count(), 2)


# ======================================================================
# Registration flow (via views)
# ======================================================================

class RegistrationViewTests(BaseAccountTestCase):
    """Tests for the signup view at /signup/."""

    def test_signup_page_loads(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.Utils.send_email')
    def test_register_success(self, mock_email):
        response = self.client.post('/signup/', {
            'email': 'newuser@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(email='newuser@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_confirm)
        self.assertIsNotNone(user.verification_code)
        self.assertIsNotNone(user.api_token)
        mock_email.assert_called_once()

    def test_register_missing_email(self):
        response = self.client.post('/signup/', {'password': 'testpass123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.filter(email='').count(), 0)

    def test_register_missing_password(self):
        response = self.client.post('/signup/', {'email': 'nopass@example.com'})
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
        response = self.client.get('/account/')
        # After registration user is logged in, but may redirect to verify
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 302:
            self.assertIn('verify', response.url)

    @patch('app.utils.Utils.send_email')
    def test_register_email_case_insensitive(self, mock_email):
        self.client.post('/signup/', {
            'email': 'CaseTest@Example.com',
            'password': 'testpass123',
        })
        user = CustomUser.objects.get(email='casetest@example.com')
        self.assertEqual(user.email, 'casetest@example.com')

    def test_signup_redirect_if_authenticated(self):
        user = CustomUser.objects.create_user(
            email='already@example.com', password='testpass123'
        )
        self.client.force_login(user)
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 302)


# ======================================================================
# Login / Logout flow
# ======================================================================

class LoginViewTests(BaseAccountTestCase):
    """Tests for login and logout views."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='login@example.com', password='testpass123'
        )

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects(self):
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
        self.assertEqual(response.status_code, 200)

    def test_login_nonexistent_user(self):
        response = self.client.post('/login/', {
            'email': 'nobody@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_missing_email(self):
        response = self.client.post('/login/', {'password': 'testpass123'})
        self.assertEqual(response.status_code, 200)

    def test_login_missing_password(self):
        response = self.client.post('/login/', {'email': 'login@example.com'})
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_if_already_authenticated(self):
        self.client.login(email='login@example.com', password='testpass123')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)

    def test_login_post_redirect_if_already_authenticated(self):
        self.client.login(email='login@example.com', password='testpass123')
        response = self.client.post('/login/', {
            'email': 'login@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(email='login@example.com', password='testpass123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        # After logout, account page should redirect to login
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)

    def test_login_email_case_insensitive(self):
        """Login should work regardless of email case."""
        response = self.client.post('/login/', {
            'email': 'LOGIN@example.com',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)


# ======================================================================
# Email verification
# ======================================================================

class EmailVerificationViewTests(BaseAccountTestCase):
    """Tests for email verification at /verify/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='verify@example.com', password='testpass123'
        )
        cls.user.is_confirm = False
        cls.user.verification_code = '123456'
        cls.user.save()

    def test_verify_page_redirects_unauthenticated(self):
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 302)

    def test_verify_page_loads_when_logged_in(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 200)

    def test_verify_correct_code_redirects(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.post('/verify/', {'code': '123456'})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_confirm)

    def test_verify_wrong_code_stays_on_page(self):
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.post('/verify/', {'code': '999999'})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_confirm)

    def test_verified_user_redirects_from_verify(self):
        self.user.is_confirm = True
        self.user.save()
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.get('/verify/')
        self.assertEqual(response.status_code, 302)

    def test_verify_post_unauthenticated_redirects(self):
        response = self.client.post('/verify/', {'code': '123456'})
        self.assertEqual(response.status_code, 302)

    def test_verify_post_already_confirmed_redirects(self):
        self.user.is_confirm = True
        self.user.save()
        self.client.login(email='verify@example.com', password='testpass123')
        response = self.client.post('/verify/', {'code': '123456'})
        self.assertEqual(response.status_code, 302)


# ======================================================================
# Password reset flow
# ======================================================================

class PasswordResetViewTests(BaseAccountTestCase):
    """Tests for lost-password and restore-password flows."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='reset@example.com', password='oldpass123'
        )

    def test_lost_password_page_loads(self):
        response = self.client.get('/lost-password/')
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.Utils.send_email')
    def test_lost_password_valid_email(self, mock_email):
        response = self.client.post('/lost-password/', {
            'email': 'reset@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.restore_password_token)
        mock_email.assert_called_once()

    def test_lost_password_unknown_email(self):
        response = self.client.post('/lost-password/', {
            'email': 'unknown@example.com',
        })
        self.assertEqual(response.status_code, 200)

    def test_lost_password_empty_email(self):
        response = self.client.post('/lost-password/', {'email': ''})
        self.assertEqual(response.status_code, 200)

    def test_lost_password_invalid_email_format(self):
        response = self.client.post('/lost-password/', {
            'email': 'not-valid',
        })
        self.assertEqual(response.status_code, 200)

    @patch('app.utils.Utils.send_email')
    def test_lost_password_rate_limit(self, mock_email):
        """Sending reset email twice within 10 minutes should fail."""
        self.user.lost_password_email_sent_at = timezone.now()
        self.user.save()
        response = self.client.post('/lost-password/', {
            'email': 'reset@example.com',
        })
        self.assertEqual(response.status_code, 200)
        # Email should not be sent a second time
        mock_email.assert_not_called()

    def test_lost_password_redirect_if_authenticated(self):
        self.client.login(email='reset@example.com', password='oldpass123')
        response = self.client.get('/lost-password/')
        self.assertEqual(response.status_code, 302)

    def test_restore_password_page_requires_token(self):
        """GET /restore-password/ without token redirects unauthenticated users."""
        response = self.client.get('/restore-password/')
        self.assertEqual(response.status_code, 302)

    def test_restore_password_page_with_token(self):
        response = self.client.get('/restore-password/', {'token': 'test-token'})
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
        token = 'test-reset-token-mismatch'
        self.user.restore_password_token = token
        self.user.save()
        response = self.client.post('/restore-password/', {
            'token': token,
            'password': 'newpass123',
            'confirm_password': 'differentpass',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass123'))

    def test_restore_password_invalid_token(self):
        response = self.client.post('/restore-password/', {
            'token': 'nonexistent-token',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
        })
        self.assertEqual(response.status_code, 200)

    def test_restore_password_short_password(self):
        token = 'test-reset-token-short'
        self.user.restore_password_token = token
        self.user.save()
        response = self.client.post('/restore-password/', {
            'token': token,
            'password': 'ab',
            'confirm_password': 'ab',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        # Password should NOT have changed
        self.assertTrue(self.user.check_password('oldpass123'))


# ======================================================================
# Password update (logged-in user)
# ======================================================================

class PasswordUpdateTests(BaseAccountTestCase):
    """Tests for CustomUser.update_password (change password while logged in)."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='pwupdate@example.com', password='oldpass123'
        )

    def test_update_password_success(self):
        self.client.force_login(self.user)
        result, msg = CustomUser.update_password(self.user, {
            'password': 'oldpass123',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123',
        }, settings={'i18n': {}})
        self.assertIsNotNone(result)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    def test_update_password_wrong_current(self):
        self.client.force_login(self.user)
        result, errors = CustomUser.update_password(self.user, {
            'password': 'wrongold',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123',
        }, settings={'i18n': {}})
        self.assertIsNone(result)
        self.assertIsNotNone(errors)

    def test_update_password_mismatch_new(self):
        self.client.force_login(self.user)
        result, errors = CustomUser.update_password(self.user, {
            'password': 'oldpass123',
            'new_password': 'newpass123',
            'confirm_password': 'differentpass',
        }, settings={'i18n': {}})
        self.assertIsNone(result)
        self.assertIsNotNone(errors)

    def test_update_password_missing_fields(self):
        self.client.force_login(self.user)
        result, errors = CustomUser.update_password(self.user, {}, settings={'i18n': {}})
        self.assertIsNone(result)
        self.assertTrue(len(errors) > 0)


# ======================================================================
# Resend verification email
# ======================================================================

class ResendVerificationTests(BaseAccountTestCase):
    """Tests for the resend-verification API endpoint."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='resend@example.com', password='testpass123'
        )

    @patch('app.utils.Utils.send_email')
    def test_resend_verification_authenticated(self, mock_email):
        self.client.force_login(self.user)
        response = self.client.post('/api/accounts/resend-verification/')
        self.assertEqual(response.status_code, 200)


# ======================================================================
# Account page access
# ======================================================================

class AccountPageTests(BaseAccountTestCase):
    """Tests for the account page access control."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.verified_user = CustomUser.objects.create_user(
            email='verified@example.com', password='testpass123'
        )
        cls.verified_user.is_confirm = True
        cls.verified_user.save()

        cls.unverified_user = CustomUser.objects.create_user(
            email='unverified@example.com', password='testpass123'
        )

    def test_account_requires_login(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_account_unverified_redirects_to_verify(self):
        self.client.login(email='unverified@example.com', password='testpass123')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('verify', response.url)

    def test_account_verified_shows_page(self):
        self.client.login(email='verified@example.com', password='testpass123')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)


# ======================================================================
# Account deletion
# ======================================================================

class DeleteAccountTests(BaseAccountTestCase):
    """Tests for account deletion at /delete-account/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_delete_page_requires_login(self):
        response = self.client.get('/delete-account/')
        self.assertEqual(response.status_code, 302)

    def test_delete_page_loads_when_authenticated(self):
        user = CustomUser.objects.create_user(
            email='deletetest@example.com', password='testpass123'
        )
        self.client.force_login(user)
        response = self.client.get('/delete-account/')
        self.assertEqual(response.status_code, 200)

    def test_delete_account_post(self):
        user = CustomUser.objects.create_user(
            email='tobedeleted@example.com', password='testpass123'
        )
        self.client.force_login(user)
        response = self.client.post('/delete-account/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CustomUser.objects.filter(email='tobedeleted@example.com').exists())


# ======================================================================
# Cancel subscription page
# ======================================================================

class CancelSubscriptionViewTests(BaseAccountTestCase):
    """Tests for the cancel subscription page."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='cancelsub@example.com', password='testpass123'
        )
        cls.user.is_plan_active = True
        cls.user.processor = 'stripe'
        cls.user.save()

    def test_cancel_page_requires_auth(self):
        response = self.client.get('/cancel/')
        self.assertEqual(response.status_code, 302)

    def test_cancel_page_loads_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get('/cancel/')
        self.assertEqual(response.status_code, 200)

    def test_cancel_post_deactivates_plan(self):
        self.client.force_login(self.user)
        response = self.client.post('/cancel/')
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_plan_active)


# ======================================================================
# CreditsConsume API endpoint
# ======================================================================

class CreditsConsumeAPITests(BaseAccountTestCase):
    """Tests for the POST /api/accounts/consume/ endpoint."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='consume@example.com', password='testpass123'
        )
        cls.user.credits = 5
        cls.user.save()

    def test_consume_endpoint_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/accounts/consume/')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 4)

    def test_consume_endpoint_unauthenticated(self):
        """Unauthenticated consume should still succeed but not crash."""
        response = self.client.post('/api/accounts/consume/')
        # consume_credits handles None user gracefully
        self.assertEqual(response.status_code, 200)


# ======================================================================
# CancelSubscription API endpoint
# ======================================================================

class CancelSubscriptionAPITests(BaseAccountTestCase):
    """Tests for POST /api/accounts/cancel-subscription/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='cancelapi@example.com', password='testpass123'
        )
        cls.user.is_plan_active = True
        cls.user.save()

    def test_cancel_api_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/accounts/cancel-subscription/')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_plan_active)
