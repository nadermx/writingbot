import hashlib
import logging

from django.conf import settings as django_settings
from django.utils import timezone

from ai_tools.generators import GENERATOR_REGISTRY, CATEGORY_NAMES
from ai_tools.models import GenerationHistory, DailyUsage

logger = logging.getLogger('app')

TOOL_LIMITS = django_settings.TOOL_LIMITS.get('ai_tools', {})
FREE_DAILY_LIMIT = TOOL_LIMITS.get('free_daily', 50)


class AIToolsService:
    """Service layer for AI tools usage tracking and generation."""

    @staticmethod
    def get_ip_hash(ip, user_agent=''):
        """Hash IP + user-agent for anonymous rate limiting."""
        raw = f'{ip}:{user_agent}'
        return hashlib.sha256(raw.encode()).hexdigest()

    @staticmethod
    def check_daily_usage(user, ip, user_agent=''):
        """
        Return the current daily usage count for a user or anonymous IP.

        Args:
            user: The request user (may be anonymous).
            ip: Client IP address.
            user_agent: Client user-agent string.

        Returns:
            int: Number of generations used today.
        """
        today = timezone.now().date()

        if user and user.is_authenticated:
            usage, _ = DailyUsage.objects.get_or_create(
                user=user, date=today,
                defaults={'count': 0},
            )
        else:
            ip_hash = AIToolsService.get_ip_hash(ip, user_agent)
            usage, _ = DailyUsage.objects.get_or_create(
                ip_hash=ip_hash, date=today, user=None,
                defaults={'count': 0},
            )

        return usage.count

    @staticmethod
    def check_daily_limit(user, ip, user_agent=''):
        """
        Check if the user/IP has exceeded their daily generation limit.

        Returns:
            Tuple of (allowed: bool, remaining: int, limit: int).
            For premium users, remaining and limit are -1 (unlimited).
        """
        is_premium = (
            user and user.is_authenticated
            and getattr(user, 'is_plan_active', False)
        )

        if is_premium:
            return True, -1, -1

        limit = FREE_DAILY_LIMIT
        count = AIToolsService.check_daily_usage(user, ip, user_agent)
        remaining = max(0, limit - count)
        return count < limit, remaining, limit

    @staticmethod
    def increment_usage(user, ip, user_agent=''):
        """Increment the daily usage counter for this user/IP."""
        today = timezone.now().date()

        if user and user.is_authenticated:
            usage, _ = DailyUsage.objects.get_or_create(
                user=user, date=today,
                defaults={'count': 0},
            )
        else:
            ip_hash = AIToolsService.get_ip_hash(ip, user_agent)
            usage, _ = DailyUsage.objects.get_or_create(
                ip_hash=ip_hash, date=today, user=None,
                defaults={'count': 0},
            )

        usage.count += 1
        usage.save(update_fields=['count'])

    @staticmethod
    def save_history(user, tool_slug, input_params, output_text):
        """Save a generation to history."""
        GenerationHistory.objects.create(
            user=user if user and user.is_authenticated else None,
            tool_slug=tool_slug,
            input_params=input_params,
            output_text=output_text,
        )

    @staticmethod
    def generate(slug, params, user=None, ip='', user_agent=''):
        """
        Look up generator, check daily limit, call generate(), save history.

        Args:
            slug: The generator slug.
            params: Dict of user input parameters.
            user: The request user (may be None/anonymous).
            ip: Client IP address.
            user_agent: Client user-agent string.

        Returns:
            Tuple of (output_text, error).
        """
        generator = GENERATOR_REGISTRY.get(slug)
        if not generator:
            return None, f'Unknown tool: {slug}'

        # Check daily limits
        allowed, remaining, limit = AIToolsService.check_daily_limit(user, ip, user_agent)
        if not allowed:
            return None, f'Daily limit of {limit} free generations reached. Upgrade to Premium for unlimited access.'

        # Generate content
        output_text, error = generator.generate(params)

        if error:
            return None, error

        # Track usage and save history
        AIToolsService.increment_usage(user, ip, user_agent)
        AIToolsService.save_history(user, slug, params, output_text)

        return output_text, None

    @staticmethod
    def get_generators_by_category():
        """
        Return generators grouped by category with display names.

        Returns:
            dict: {category_key: {'name': display_name, 'generators': [generator_dicts]}}
        """
        grouped = {}
        for slug, gen in GENERATOR_REGISTRY.items():
            cat = gen.category
            if cat not in grouped:
                grouped[cat] = {
                    'name': CATEGORY_NAMES.get(cat, cat),
                    'generators': [],
                }
            grouped[cat]['generators'].append(gen.to_dict())

        # Return in a consistent category order
        ordered = {}
        for cat_key in CATEGORY_NAMES:
            if cat_key in grouped:
                ordered[cat_key] = grouped[cat_key]
        return ordered
