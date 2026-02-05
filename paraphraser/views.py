import logging

from django.conf import settings as django_settings
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from paraphraser.models import ParaphraseHistory
from paraphraser.services import AIParaphraseService
import config

logger = logging.getLogger('app')

# Tool limits from settings
TOOL_LIMITS = django_settings.TOOL_LIMITS.get('paraphraser', {})
FREE_WORD_LIMIT = TOOL_LIMITS.get('free_words', 500)
FREE_MODES = TOOL_LIMITS.get('free_modes', ['standard', 'fluency'])

ALL_MODES = [
    'standard', 'fluency', 'formal', 'academic', 'simple',
    'creative', 'expand', 'shorten', 'custom', 'humanizer',
]


class ParaphraserPage(View):
    """Renders the main paraphraser tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        return render(
            request,
            'tools/paraphraser.html',
            {
                'title': f"Paraphrasing Tool | {config.PROJECT_NAME}",
                'description': 'Free online paraphrasing tool powered by AI. Rewrite text in 10 different modes with synonym control and word freezing.',
                'page': 'paraphraser',
                'g': g,
                'is_premium': is_premium,
                'free_word_limit': FREE_WORD_LIMIT,
                'free_modes': FREE_MODES,
                'all_modes': ALL_MODES,
            }
        )


class ParaphraseAPI(APIView):
    """
    POST /api/paraphrase/
    Accepts text and settings, returns paraphrased output.
    """

    def post(self, request):
        data = request.data
        text = data.get('text', '').strip()
        mode = data.get('mode', 'standard')
        synonym_level = data.get('synonym_level', 3)
        frozen_words = data.get('frozen_words', [])
        settings_dict = data.get('settings', {})
        language = data.get('language', 'en')

        # --- Validation ---
        if not text:
            return Response(
                {'error': 'Please enter some text to paraphrase.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if mode not in ALL_MODES:
            return Response(
                {'error': 'Invalid paraphrasing mode.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            synonym_level = int(synonym_level)
            synonym_level = max(1, min(5, synonym_level))
        except (ValueError, TypeError):
            synonym_level = 3

        word_count = AIParaphraseService.count_words(text)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )

        # --- Free tier limits ---
        if not is_premium:
            if word_count > FREE_WORD_LIMIT:
                return Response(
                    {
                        'error': f'Free accounts are limited to {FREE_WORD_LIMIT} words. You entered {word_count} words.',
                        'upgrade': True,
                        'word_count': word_count,
                        'limit': FREE_WORD_LIMIT,
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            if mode not in FREE_MODES:
                return Response(
                    {
                        'error': f'The "{mode}" mode is available for premium users only.',
                        'upgrade': True,
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        # --- Call AI service ---
        output_text, error = AIParaphraseService.paraphrase(
            text=text,
            mode=mode,
            synonym_level=synonym_level,
            frozen_words=frozen_words,
            settings_dict=settings_dict,
            language=language,
            use_premium=is_premium,
        )

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # --- Save history for authenticated users ---
        if request.user.is_authenticated:
            try:
                ParaphraseHistory.objects.create(
                    user=request.user,
                    input_text=text,
                    output_text=output_text,
                    mode=mode,
                    synonym_level=synonym_level,
                    frozen_words=frozen_words,
                    settings=settings_dict,
                    language=language,
                    word_count=word_count,
                )
            except Exception as e:
                logger.error(f'Failed to save paraphrase history: {e}')

        return Response({
            'output_text': output_text,
            'input_word_count': word_count,
            'output_word_count': AIParaphraseService.count_words(output_text),
            'mode': mode,
        })


class SynonymAPI(APIView):
    """
    POST /api/paraphrase/synonyms/
    Returns contextual synonyms for a clicked word.
    """

    def post(self, request):
        data = request.data
        word = data.get('word', '').strip()
        context = data.get('context', '').strip()

        if not word:
            return Response(
                {'error': 'No word provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        synonyms, error = AIParaphraseService.get_synonyms(word, context)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'word': word,
            'synonyms': synonyms,
        })


class HistoryAPI(APIView):
    """
    GET /api/paraphrase/history/
    Returns the authenticated user's paraphrase history (premium only).
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not request.user.is_plan_active:
            return Response(
                {'error': 'History is available for premium users only.', 'upgrade': True},
                status=status.HTTP_403_FORBIDDEN
            )

        page = int(request.GET.get('page', 1))
        per_page = 20
        offset = (page - 1) * per_page

        entries = ParaphraseHistory.objects.filter(
            user=request.user
        ).order_by('-created_at')[offset:offset + per_page]

        total = ParaphraseHistory.objects.filter(user=request.user).count()

        return Response({
            'history': [
                {
                    'id': entry.id,
                    'input_text': entry.input_text[:200],
                    'output_text': entry.output_text[:200],
                    'mode': entry.mode,
                    'word_count': entry.word_count,
                    'created_at': entry.created_at.isoformat(),
                }
                for entry in entries
            ],
            'total': total,
            'page': page,
            'per_page': per_page,
        })
