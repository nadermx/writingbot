import logging
from django.views import View
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.views import GlobalVars
from grammar.models import GrammarCheckHistory
from grammar.services import AIGrammarService

logger = logging.getLogger('app')


class GrammarPage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )

        context = {
            'g': g,
            'title': f"{g.get('i18n', {}).get('grammar_checker', 'Grammar Checker')} - {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free online grammar checker. Fix grammar, spelling, and punctuation errors instantly with AI-powered writing analysis.',
            'page': 'grammar',
            'is_premium': is_premium,
            'word_limit': settings.TOOL_LIMITS['grammar']['free_words'],
        }
        return render(request, 'tools/grammar.html', context)


class GrammarCheckAPI(APIView):
    def post(self, request):
        text = request.data.get('text', '').strip()
        dialect = request.data.get('dialect', 'en-us')

        if not text:
            return Response(
                {'error': 'Please enter some text to check.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Word count check
        word_count = len(text.split())
        free_limit = settings.TOOL_LIMITS['grammar']['free_words']
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )

        if not is_premium and word_count > free_limit:
            return Response(
                {
                    'error': f'Free accounts are limited to {free_limit} words. You entered {word_count} words.',
                    'upgrade': True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        service = AIGrammarService()
        result, error = service.check_grammar(text, dialect)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save history
        try:
            GrammarCheckHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                corrections=result.get('corrections', []),
                writing_score=result.get('writing_scores', {}),
                word_count=word_count,
            )
        except Exception as e:
            logger.error(f"Failed to save grammar check history: {e}")

        return Response({
            'corrections': result.get('corrections', []),
            'writing_scores': result.get('writing_scores', {}),
            'tone': result.get('tone', 'neutral'),
            'readability_score': result.get('readability_score', 50),
            'word_count': word_count,
        })


class GrammarFixAPI(APIView):
    def post(self, request):
        text = request.data.get('text', '').strip()
        corrections = request.data.get('corrections', [])
        fix_mode = request.data.get('mode', 'all')  # 'all' or 'single'
        correction = request.data.get('correction', None)

        if not text:
            return Response(
                {'error': 'No text provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = AIGrammarService()

        if fix_mode == 'single' and correction:
            fixed_text, error = service.fix_single(text, correction)
        else:
            fixed_text, error = service.fix_all(text, corrections)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'fixed_text': fixed_text,
        })
