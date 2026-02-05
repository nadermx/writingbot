import logging

from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from ai_tools.generators import GENERATOR_REGISTRY, CATEGORY_NAMES
from ai_tools.services import AIToolsService
from app.utils import Utils
import config

logger = logging.getLogger('app')


class AIToolsIndexPage(View):
    """GET /ai-writing-tools/ - Renders the index page listing all tools by category."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        categories = AIToolsService.get_generators_by_category()
        total = len(GENERATOR_REGISTRY)

        context = {
            'g': g,
            'title': f'AI Writing Tools ({total}+ Free Tools) - {config.PROJECT_NAME}',
            'description': f'Free AI writing tools: essay writer, blog generator, email writer, and {total}+ more. Generate any type of content instantly with AI.',
            'page': 'ai-tools',
            'categories': categories,
            'total_tools': total,
        }
        return render(request, 'ai-tools/index.html', context)


class AIToolPage(View):
    """GET /ai-writing-tools/<slug>/ - Renders the individual tool generator page."""

    def get(self, request, slug):
        g = GlobalVars.get_globals(request)
        generator = GENERATOR_REGISTRY.get(slug)

        if not generator:
            return render(request, '404.html', {'g': g}, status=404)

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )

        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = AIToolsService.check_daily_limit(
            request.user, ip, user_agent,
        )

        # Related tools from the same category (up to 6)
        related = []
        for s, gen in GENERATOR_REGISTRY.items():
            if gen.category == generator.category and s != slug:
                related.append(gen.to_dict())
                if len(related) >= 6:
                    break

        context = {
            'g': g,
            'title': generator.meta_title,
            'description': generator.meta_description,
            'page': 'ai-tools',
            'tool': generator.to_dict(),
            'is_premium': is_premium,
            'remaining': remaining,
            'limit': limit,
            'related_tools': related,
        }
        return render(request, 'ai-tools/generator.html', context)


class AIToolGenerateAPI(APIView):
    """POST /api/ai-tools/generate/ - Validates limit, generates content, returns JSON."""

    def post(self, request):
        tool_slug = request.data.get('tool', '').strip()
        if not tool_slug:
            return Response(
                {'error': 'The "tool" field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        generator = GENERATOR_REGISTRY.get(tool_slug)
        if not generator:
            return Response(
                {'error': f'Unknown tool: {tool_slug}'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Extract and validate parameters
        params = {}
        for field in generator.fields:
            raw = request.data.get(field['name'], '')
            value = raw.strip() if isinstance(raw, str) else raw
            if field.get('required') and not value:
                return Response(
                    {'error': f'The "{field["label"]}" field is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            params[field['name']] = value

        # Include tone if provided separately
        tone = request.data.get('tone', '')
        if tone:
            params['tone'] = tone

        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        output_text, error = AIToolsService.generate(
            slug=tool_slug,
            params=params,
            user=request.user,
            ip=ip,
            user_agent=user_agent,
        )

        if error:
            if 'Daily limit' in error:
                return Response(
                    {'error': error, 'upgrade': True},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return remaining count after generation
        allowed, remaining, limit = AIToolsService.check_daily_limit(
            request.user, ip, user_agent,
        )

        return Response({
            'output': output_text,
            'tool': tool_slug,
            'remaining': remaining,
            'limit': limit,
        })
