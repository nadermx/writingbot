import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from api.authentication import APIKeyAuthentication
from api.throttling import APIRateThrottle
import config

logger = logging.getLogger('app')


class APIDocsPage(View):
    """Renders the API documentation page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        api_token = ''
        if request.user.is_authenticated:
            api_token = request.user.api_token or ''

        return render(request, 'api/docs.html', {
            'title': f'API Documentation | {config.PROJECT_NAME}',
            'description': f'{config.PROJECT_NAME} API - Paraphrase, check grammar, summarize, detect AI content, and translate text programmatically.',
            'page': 'api-docs',
            'g': g,
            'api_token': api_token,
        })


class BasePublicAPIView(APIView):
    """Base class for all public API v1 endpoints."""
    authentication_classes = [APIKeyAuthentication]
    throttle_classes = [APIRateThrottle]

    def get_user_limits(self, request):
        """Return whether the user is premium."""
        if request.user and request.user.is_authenticated:
            return request.user.is_plan_active
        return False


class ParaphraseAPIv1(BasePublicAPIView):
    """
    POST /api/v1/paraphrase/
    Public API for paraphrasing text.
    """

    def post(self, request):
        from paraphraser.services import AIParaphraseService

        text = request.data.get('text', '').strip()
        mode = request.data.get('mode', 'standard')
        synonym_level = request.data.get('synonym_level', 3)
        language = request.data.get('language', 'en')

        if not text:
            return Response(
                {'error': 'The "text" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = self.get_user_limits(request)

        # Enforce limits
        word_count = AIParaphraseService.count_words(text)
        if not is_premium and word_count > 500:
            return Response(
                {'error': 'Free API users are limited to 500 words per request.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        valid_modes = ['standard', 'fluency', 'formal', 'academic', 'simple',
                       'creative', 'expand', 'shorten']
        if mode not in valid_modes:
            return Response(
                {'error': f'Invalid mode. Valid modes: {", ".join(valid_modes)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not is_premium and mode not in ['standard', 'fluency']:
            return Response(
                {'error': f'The "{mode}" mode requires a premium API plan.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            synonym_level = max(1, min(5, int(synonym_level)))
        except (ValueError, TypeError):
            synonym_level = 3

        output_text, error = AIParaphraseService.paraphrase(
            text=text, mode=mode, synonym_level=synonym_level, language=language,
        )

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'output_text': output_text,
            'input_word_count': word_count,
            'output_word_count': AIParaphraseService.count_words(output_text),
            'mode': mode,
        })


class GrammarAPIv1(BasePublicAPIView):
    """
    POST /api/v1/grammar/
    Public API for grammar checking.
    """

    def post(self, request):
        from grammar.services import AIGrammarService

        text = request.data.get('text', '').strip()
        language = request.data.get('language', 'en')

        if not text:
            return Response(
                {'error': 'The "text" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = self.get_user_limits(request)
        word_count = len(text.split())

        if not is_premium and word_count > 5000:
            return Response(
                {'error': 'Free API users are limited to 5000 words per request.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        result, error = AIGrammarService.check_grammar(text=text, language=language)

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result)


class SummarizeAPIv1(BasePublicAPIView):
    """
    POST /api/v1/summarize/
    Public API for text summarization.
    """

    def post(self, request):
        from summarizer.services import AISummarizerService

        text = request.data.get('text', '').strip()
        mode = request.data.get('mode', 'paragraph')
        length = request.data.get('length', 50)
        language = request.data.get('language', 'en')

        if not text:
            return Response(
                {'error': 'The "text" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = self.get_user_limits(request)
        word_count = len(text.split())

        max_words = 6000 if is_premium else 1200
        if word_count > max_words:
            return Response(
                {'error': f'Text exceeds the {max_words}-word limit.', 'upgrade': not is_premium},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            length = max(10, min(100, int(length)))
        except (ValueError, TypeError):
            length = 50

        summary, error = AISummarizerService.summarize(
            text=text, mode=mode, length=length, language=language,
        )

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'summary': summary,
            'input_word_count': word_count,
            'mode': mode,
        })


class AIDetectAPIv1(BasePublicAPIView):
    """
    POST /api/v1/ai-detect/
    Public API for AI content detection.
    """

    def post(self, request):
        from ai_detector.services import AIDetectorService

        text = request.data.get('text', '').strip()

        if not text:
            return Response(
                {'error': 'The "text" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = self.get_user_limits(request)
        word_count = len(text.split())

        if not is_premium and word_count > 1200:
            return Response(
                {'error': 'Free API users are limited to 1200 words per request.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        result, error = AIDetectorService.detect(text=text)

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(result)


class TranslateAPIv1(BasePublicAPIView):
    """
    POST /api/v1/translate/
    Public API for text translation.
    """

    def post(self, request):
        from translator.services import TranslationService

        text = request.data.get('text', '').strip()
        source_lang = request.data.get('source_lang', 'auto')
        target_lang = request.data.get('target_lang', '')

        if not text:
            return Response(
                {'error': 'The "text" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not target_lang:
            return Response(
                {'error': 'The "target_lang" field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = self.get_user_limits(request)

        if not is_premium and len(text) > 5000:
            return Response(
                {'error': 'Free API users are limited to 5000 characters per request.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        result, error = TranslationService.translate(
            text=text, source_lang=source_lang, target_lang=target_lang,
            use_premium=is_premium,
        )

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'translated_text': result['translated_text'],
            'source_lang': result['source_lang'],
            'target_lang': result['target_lang'],
            'character_count': len(text),
        })
