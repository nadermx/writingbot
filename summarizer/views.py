import logging
from django.views import View
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.views import GlobalVars
from summarizer.models import SummaryHistory
from summarizer.services import AISummarizerService

logger = logging.getLogger('app')


class SummarizerPage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )

        limits = settings.TOOL_LIMITS['summarizer']
        word_limit = limits['premium_words'] if is_premium else limits['free_words']

        context = {
            'g': g,
            'title': f"{g.get('i18n', {}).get('summarizer', 'Summarizer')} - {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free AI text summarizer. Condense articles, papers, and documents into key sentences or concise paragraphs.',
            'page': 'summarizer',
            'is_premium': is_premium,
            'word_limit': word_limit,
        }
        return render(request, 'tools/summarizer.html', context)


class SummarizeAPI(APIView):
    def post(self, request):
        text = request.data.get('text', '').strip()
        mode = request.data.get('mode', 'paragraph')
        length = request.data.get('length', 3)

        if not text:
            return Response(
                {'error': 'Please enter some text to summarize.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate mode
        if mode not in ('key_sentences', 'paragraph'):
            mode = 'paragraph'

        # Validate length
        try:
            length = max(1, min(5, int(length)))
        except (TypeError, ValueError):
            length = 3

        # Word count check
        word_count = len(text.split())
        limits = settings.TOOL_LIMITS['summarizer']
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )
        word_limit = limits['premium_words'] if is_premium else limits['free_words']

        if word_count > word_limit:
            return Response(
                {
                    'error': f'{"Premium" if is_premium else "Free"} accounts are limited to {word_limit} words. You entered {word_count} words.',
                    'upgrade': not is_premium
                },
                status=status.HTTP_403_FORBIDDEN
            )

        service = AISummarizerService()
        result, error = service.summarize(text, mode, length, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save history
        try:
            SummaryHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                output_text=result.get('summary', ''),
                mode=mode,
                summary_length=length,
                word_count=word_count,
            )
        except Exception as e:
            logger.error(f"Failed to save summary history: {e}")

        return Response(result)
