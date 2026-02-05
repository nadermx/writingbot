"""
Usage tracking utilities for WritingBot.ai
Tracks per-tool, per-user usage for rate limiting and analytics.
"""
import logging
from hashlib import md5
from django.utils import timezone
from django.core.cache import cache

logger = logging.getLogger('app')


class UsageTracker:
    """Track tool usage per user/IP for rate limiting."""

    @staticmethod
    def get_cache_key(tool, user=None, ip=None):
        """Generate a unique cache key for usage tracking."""
        date_str = timezone.now().strftime('%Y-%m-%d')
        if user and user.is_authenticated:
            identifier = f'user:{user.id}'
        elif ip:
            identifier = f'ip:{md5(ip.encode()).hexdigest()}'
        else:
            identifier = 'anon'
        return f'usage:{tool}:{identifier}:{date_str}'

    @staticmethod
    def get_monthly_cache_key(tool, user):
        """Generate monthly cache key for tools with monthly limits."""
        month_str = timezone.now().strftime('%Y-%m')
        return f'usage_monthly:{tool}:user:{user.id}:{month_str}'

    @staticmethod
    def get_daily_count(tool, user=None, ip=None):
        """Get today's usage count for a tool."""
        key = UsageTracker.get_cache_key(tool, user, ip)
        return cache.get(key, 0)

    @staticmethod
    def increment_daily(tool, user=None, ip=None, amount=1):
        """Increment today's usage count."""
        key = UsageTracker.get_cache_key(tool, user, ip)
        current = cache.get(key, 0)
        # Set with 24-hour expiry
        cache.set(key, current + amount, timeout=86400)
        return current + amount

    @staticmethod
    def get_monthly_count(tool, user):
        """Get this month's usage count for a tool."""
        key = UsageTracker.get_monthly_cache_key(tool, user)
        return cache.get(key, 0)

    @staticmethod
    def increment_monthly(tool, user, amount=1):
        """Increment this month's usage count."""
        key = UsageTracker.get_monthly_cache_key(tool, user)
        current = cache.get(key, 0)
        # Set with 31-day expiry
        cache.set(key, current + amount, timeout=2678400)
        return current + amount

    @staticmethod
    def check_daily_limit(tool, limit, user=None, ip=None):
        """
        Check if user is within daily limit.
        Returns (allowed, current_count, limit).
        Premium users (limit=None) always pass.
        """
        if limit is None:
            return True, 0, None
        current = UsageTracker.get_daily_count(tool, user, ip)
        return current < limit, current, limit

    @staticmethod
    def check_monthly_limit(tool, limit, user=None):
        """
        Check if user is within monthly limit.
        Returns (allowed, current_count, limit).
        """
        if limit is None or user is None:
            return True, 0, None
        current = UsageTracker.get_monthly_count(tool, user)
        return current < limit, current, limit
