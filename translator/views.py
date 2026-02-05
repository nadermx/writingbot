import json
import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from translator.models import TranslationHistory
from translator.services import TranslationService
import config

logger = logging.getLogger('app')


class TranslatorPage(View):
    def get(self, request):
        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        languages = TranslationService.get_languages()
        return render(
            request,
            'tools/translator.html',
            {
                'title': f"Translator | {config.PROJECT_NAME}",
                'description': 'Translate text between 60+ languages instantly. Free online translator powered by AI.',
                'page': 'translator',
                'g': settings,
                'is_premium': is_premium,
                'languages_json': json.dumps(languages),
            }
        )


class TranslateAPI(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', '')

        if not text:
            return Response(
                {'error': 'Please provide text to translate.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not target_lang:
            return Response(
                {'error': 'Please select a target language.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        char_count = len(text)

        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )

        # Character limit for free users
        if not is_premium and char_count > 5000:
            return Response(
                {
                    'error': 'Free users are limited to 5,000 characters. Upgrade to Premium for unlimited translations.',
                    'limit_exceeded': True,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Run translation
        result, error = TranslationService.translate(text, source_lang, target_lang)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save history
        try:
            TranslationHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                output_text=result['translated_text'],
                source_lang=result['source_lang'],
                target_lang=result['target_lang'],
                char_count=char_count,
            )
        except Exception as e:
            logger.error(f'Failed to save translation history: {str(e)}')

        return Response({
            'translated_text': result['translated_text'],
            'source_lang': result['source_lang'],
            'target_lang': result['target_lang'],
            'char_count': char_count,
        })


class LanguagesAPI(APIView):
    def get(self, request):
        languages = TranslationService.get_languages()
        return Response({'languages': languages})
