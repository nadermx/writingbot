import logging

from rest_framework.throttling import SimpleRateThrottle

logger = logging.getLogger('app')


class APIRateThrottle(SimpleRateThrottle):
    """
    Rate throttle for the public API.
    - Free users: 100 requests/hour
    - Premium users (is_plan_active): 1000 requests/hour
    - Unauthenticated: 20 requests/hour (by IP)
    """

    scope = 'api'

    # Default rates by scope (overridden by get_rate)
    THROTTLE_RATES = {
        'api_free': '100/hour',
        'api_premium': '1000/hour',
        'api_anon': '20/hour',
    }

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = str(request.user.pk)
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }

    def get_rate(self):
        if not hasattr(self, '_request'):
            return self.THROTTLE_RATES['api_anon']

        request = self._request
        if request.user and request.user.is_authenticated:
            if getattr(request.user, 'is_plan_active', False):
                return self.THROTTLE_RATES['api_premium']
            return self.THROTTLE_RATES['api_free']
        return self.THROTTLE_RATES['api_anon']

    def allow_request(self, request, view):
        # Store request reference so get_rate() can inspect the user
        self._request = request

        # Re-parse rate since it depends on the user
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)

    def parse_rate(self, rate):
        """
        Parse '100/hour' into (100, 3600).
        """
        if rate is None:
            return (None, None)

        num, period = rate.split('/')
        num_requests = int(num)
        duration = {
            's': 1, 'sec': 1, 'second': 1,
            'm': 60, 'min': 60, 'minute': 60,
            'h': 3600, 'hour': 3600,
            'd': 86400, 'day': 86400,
        }.get(period, 3600)

        return (num_requests, duration)
