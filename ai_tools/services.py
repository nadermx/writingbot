import hashlib
import logging

from django.conf import settings as django_settings
from django.utils import timezone

from ai_tools.models import GenerationHistory, DailyUsage

logger = logging.getLogger('app')

TOOL_LIMITS = django_settings.TOOL_LIMITS.get('ai_tools', {})
FREE_DAILY_LIMIT = TOOL_LIMITS.get('free_daily', 50)


class GeneratorRegistry:
    """
    Central registry for all AI writing tool generators.
    Lazily imports and caches generator instances on first access.
    """

    _generators = None
    _by_slug = None
    _by_category = None

    @classmethod
    def _load(cls):
        if cls._generators is not None:
            return

        from ai_tools.generators.academic import ACADEMIC_GENERATORS
        from ai_tools.generators.business import BUSINESS_GENERATORS
        from ai_tools.generators.marketing import MARKETING_GENERATORS
        from ai_tools.generators.social_media import SOCIAL_MEDIA_GENERATORS
        from ai_tools.generators.creative import CREATIVE_GENERATORS
        from ai_tools.generators.professional import PROFESSIONAL_GENERATORS
        from ai_tools.generators.content import CONTENT_GENERATORS
        from ai_tools.generators.utility import UTILITY_GENERATORS

        all_classes = (
            ACADEMIC_GENERATORS
            + BUSINESS_GENERATORS
            + MARKETING_GENERATORS
            + SOCIAL_MEDIA_GENERATORS
            + CREATIVE_GENERATORS
            + PROFESSIONAL_GENERATORS
            + CONTENT_GENERATORS
            + UTILITY_GENERATORS
        )

        cls._generators = [klass() for klass in all_classes]
        cls._by_slug = {g.slug: g for g in cls._generators}
        cls._by_category = {}
        for g in cls._generators:
            cls._by_category.setdefault(g.category, []).append(g)

    @classmethod
    def all(cls):
        """Return all generator instances."""
        cls._load()
        return cls._generators

    @classmethod
    def get(cls, slug):
        """Return a generator by slug, or None."""
        cls._load()
        return cls._by_slug.get(slug)

    @classmethod
    def by_category(cls):
        """Return generators grouped by category as an OrderedDict-like dict."""
        cls._load()
        return cls._by_category

    @classmethod
    def slugs(cls):
        """Return all registered slugs."""
        cls._load()
        return list(cls._by_slug.keys())

    @classmethod
    def count(cls):
        """Return total number of generators."""
        cls._load()
        return len(cls._generators)


class AIToolsService:
    """Service layer for AI tools usage tracking and generation."""

    @staticmethod
    def get_ip_hash(request):
        """Hash IP + user-agent for anonymous rate limiting."""
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ',' in ip:
            ip = ip.split(',')[0].strip()
        ua = request.META.get('HTTP_USER_AGENT', '')
        raw = f'{ip}:{ua}'
        return hashlib.sha256(raw.encode()).hexdigest()

    @staticmethod
    def check_daily_limit(request):
        """
        Check if the user has exceeded their daily AI tool generation limit.

        Returns:
            Tuple of (allowed: bool, remaining: int, limit: int).
        """
        today = timezone.now().date()
        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )

        if is_premium:
            return True, -1, -1  # Unlimited

        limit = FREE_DAILY_LIMIT

        if request.user.is_authenticated:
            usage, _ = DailyUsage.objects.get_or_create(
                user=request.user, date=today,
                defaults={'count': 0},
            )
        else:
            ip_hash = AIToolsService.get_ip_hash(request)
            usage, _ = DailyUsage.objects.get_or_create(
                ip_hash=ip_hash, date=today, user=None,
                defaults={'count': 0},
            )

        remaining = max(0, limit - usage.count)
        return usage.count < limit, remaining, limit

    @staticmethod
    def increment_usage(request):
        """Increment the daily usage counter for this user/IP."""
        today = timezone.now().date()

        if request.user.is_authenticated:
            usage, _ = DailyUsage.objects.get_or_create(
                user=request.user, date=today,
                defaults={'count': 0},
            )
        else:
            ip_hash = AIToolsService.get_ip_hash(request)
            usage, _ = DailyUsage.objects.get_or_create(
                ip_hash=ip_hash, date=today, user=None,
                defaults={'count': 0},
            )

        usage.count += 1
        usage.save(update_fields=['count'])

    @staticmethod
    def save_history(request, tool_slug, input_params, output_text):
        """Save a generation to history."""
        GenerationHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            tool_slug=tool_slug,
            input_params=input_params,
            output_text=output_text,
        )

    @staticmethod
    def generate(tool_slug, params, request=None):
        """
        Run a generator and return the result.

        Args:
            tool_slug: The generator slug.
            params: Dict of user input parameters.
            request: The HTTP request (for usage tracking).

        Returns:
            Tuple of (output_text, error).
        """
        generator = GeneratorRegistry.get(tool_slug)
        if not generator:
            return None, f'Unknown tool: {tool_slug}'

        # Check daily limits
        if request:
            allowed, remaining, limit = AIToolsService.check_daily_limit(request)
            if not allowed:
                return None, f'Daily limit of {limit} free generations reached. Upgrade to Premium for unlimited access.'

        # Generate content
        output_text, error = generator.generate(params)

        if error:
            return None, error

        # Track usage and save history
        if request:
            AIToolsService.increment_usage(request)
            AIToolsService.save_history(request, tool_slug, params, output_text)

        return output_text, None
