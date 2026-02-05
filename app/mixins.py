"""
Common view mixins for WritingBot.ai
"""
from django.shortcuts import redirect
from accounts.views import GlobalVars
import config


class ToolPageMixin:
    """Mixin for tool page views providing common context."""

    tool_name = ''
    tool_title = ''
    tool_description = ''
    template_name = ''

    def get_tool_context(self, request, **extra):
        settings = GlobalVars.get_globals(request)
        ctx = {
            'title': f'{self.tool_title} | {config.PROJECT_NAME}',
            'description': self.tool_description,
            'page': self.tool_name,
            'g': settings,
            'is_premium': (
                request.user.is_authenticated
                and getattr(request.user, 'is_plan_active', False)
            ),
        }
        ctx.update(extra)
        return ctx


class PremiumRequiredMixin:
    """Mixin that requires premium subscription for access."""

    def check_premium(self, request):
        if not request.user.is_authenticated:
            return False
        return getattr(request.user, 'is_plan_active', False)

    def premium_redirect(self, request):
        if not request.user.is_authenticated:
            return redirect('register')
        return redirect('pricing')
