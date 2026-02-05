import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from ai_tools.services import GeneratorRegistry, AIToolsService
import config

logger = logging.getLogger('app')


class AIToolsIndex(View):
    """Renders the AI writing tools index page with all generators grouped by category."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        categories = GeneratorRegistry.by_category()
        total = GeneratorRegistry.count()

        return render(request, 'ai-tools/index.html', {
            'title': f'AI Writing Tools ({total}+ Free Tools) | {config.PROJECT_NAME}',
            'description': f'Free AI writing tools: essay writer, blog generator, email writer, and {total}+ more. Generate any type of content instantly.',
            'page': 'ai-tools',
            'g': g,
            'categories': categories,
            'total_tools': total,
        })


class AIToolPage(View):
    """Renders an individual AI tool generator page."""

    def get(self, request, tool_slug):
        g = GlobalVars.get_globals(request)
        generator = GeneratorRegistry.get(tool_slug)

        if not generator:
            return render(request, '404.html', {'g': g}, status=404)

        is_premium = request.user.is_authenticated and request.user.is_plan_active
        allowed, remaining, limit = AIToolsService.check_daily_limit(request)

        # Get related tools from same category
        all_in_category = GeneratorRegistry.by_category().get(generator.category, [])
        related = [t for t in all_in_category if t.slug != generator.slug][:6]

        return render(request, 'ai-tools/generator.html', {
            'title': f'{generator.meta_title} | {config.PROJECT_NAME}',
            'description': generator.meta_description,
            'page': 'ai-tools',
            'g': g,
            'tool': generator.to_dict(),
            'is_premium': is_premium,
            'remaining': remaining,
            'limit': limit,
            'related_tools': [t.to_dict() for t in related],
        })


class AIToolGenerateAPI(APIView):
    """POST /api/ai-tools/generate/ - Generate content using an AI tool."""

    def post(self, request):
        tool_slug = request.data.get('tool', '').strip()
        if not tool_slug:
            return Response(
                {'error': 'The "tool" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        generator = GeneratorRegistry.get(tool_slug)
        if not generator:
            return Response(
                {'error': f'Unknown tool: {tool_slug}'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Extract parameters from request
        params = {}
        for field in generator.fields:
            value = request.data.get(field['name'], '').strip() if isinstance(request.data.get(field['name'], ''), str) else request.data.get(field['name'], '')
            if field.get('required') and not value:
                return Response(
                    {'error': f'The "{field["label"]}" field is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            params[field['name']] = value

        # Include tone if sent separately
        tone = request.data.get('tone', '')
        if tone and 'tone' not in params:
            params['tone'] = tone

        output_text, error = AIToolsService.generate(tool_slug, params, request)

        if error:
            if 'Daily limit' in error:
                return Response({'error': error, 'upgrade': True}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'output': output_text,
            'tool': tool_slug,
        })


class AIToolsListAPI(APIView):
    """GET /api/ai-tools/ - List all available AI tools."""

    def get(self, request):
        generators = GeneratorRegistry.all()
        tools = [g.to_dict() for g in generators]
        categories = {}
        for tool in tools:
            cat = tool['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'slug': tool['slug'],
                'name': tool['name'],
                'description': tool['description'],
            })

        return Response({
            'total': len(tools),
            'categories': categories,
        })
