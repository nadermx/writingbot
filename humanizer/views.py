import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from humanizer.models import HumanizeHistory
from humanizer.services import AIHumanizerService
import config

logger = logging.getLogger('app')


class HumanizerPage(View):
    def get(self, request):
        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        return render(
            request,
            'tools/humanizer.html',
            {
                'title': f"AI Humanizer | {config.PROJECT_NAME}",
                'description': 'Transform AI-generated text into natural, human-sounding writing. Bypass AI detectors with our humanizer tool.',
                'page': 'humanizer',
                'g': settings,
                'is_premium': is_premium,
            }
        )


class HumanizeAPI(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text', '').strip()
        mode = data.get('mode', 'basic')

        if not text:
            return Response(
                {'error': 'Please provide text to humanize.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if mode not in ('basic', 'advanced'):
            mode = 'basic'

        word_count = len(text.split())

        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )

        # Advanced mode requires premium
        if mode == 'advanced' and not is_premium:
            return Response(
                {
                    'error': 'Advanced mode requires a Premium subscription.',
                    'premium_required': True,
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Word limit for free users
        if not is_premium and word_count > 500:
            return Response(
                {
                    'error': 'Free users are limited to 500 words. Upgrade to Premium for unlimited humanization.',
                    'limit_exceeded': True,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Run humanization
        result, error = AIHumanizerService.humanize(text, mode)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save history
        try:
            HumanizeHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                output_text=result['output_text'],
                mode=mode,
                ai_score_before=result['ai_score_before'],
                ai_score_after=result['ai_score_after'],
            )
        except Exception as e:
            logger.error(f'Failed to save humanize history: {str(e)}')

        return Response({
            'output_text': result['output_text'],
            'ai_score_before': result['ai_score_before'],
            'ai_score_after': result['ai_score_after'],
            'word_count': word_count,
        })
