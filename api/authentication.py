import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import CustomUser

logger = logging.getLogger('app')


class APIKeyAuthentication(BaseAuthentication):
    """
    Authentication class that validates an X-API-Key header against
    CustomUser.api_token.

    Usage in views:
        authentication_classes = [APIKeyAuthentication]

    The client sends:
        X-API-Key: <their api token>
    """

    keyword = 'X-API-Key'

    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY', '').strip()

        if not api_key:
            return None  # No API key provided, skip this auth backend

        try:
            user = CustomUser.objects.get(api_token=api_key, is_active=True)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')
        except CustomUser.MultipleObjectsReturned:
            logger.error(f'Multiple users found with the same API token')
            raise AuthenticationFailed('Authentication error. Please contact support.')

        return (user, None)

    def authenticate_header(self, request):
        """
        Return a string to be used as the WWW-Authenticate header.
        """
        return self.keyword
