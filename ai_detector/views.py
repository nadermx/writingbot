import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from ai_detector.models import DetectionResult
from ai_detector.services import AIDetectorService
import config

logger = logging.getLogger('app')


class AIDetectorPage(View):
    def get(self, request):
        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        return render(
            request,
            'tools/ai-detector.html',
            {
                'title': f"AI Content Detector | {config.PROJECT_NAME}",
                'description': 'Detect AI-generated content with our advanced AI detector. Analyze text sentence by sentence to identify AI writing patterns.',
                'page': 'ai_detector',
                'g': settings,
                'is_premium': is_premium,
            }
        )


class AIDetectAPI(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text', '').strip()

        if not text:
            return Response(
                {'error': 'Please provide text to analyze.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        word_count = len(text.split())

        # Minimum word count
        if word_count < 80:
            return Response(
                {'error': 'Please enter at least 80 words for accurate detection.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Word limit based on plan
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )

        if not is_premium and word_count > 1200:
            return Response(
                {
                    'error': 'Free users are limited to 1,200 words. Upgrade to Premium for unlimited detection.',
                    'limit_exceeded': True,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Run detection
        result, error = AIDetectorService.detect(text, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save result
        try:
            DetectionResult.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                results={'sentences': result['sentences']},
                overall_score=result['overall_score'],
                classification=result['classification'],
                word_count=word_count,
            )
        except Exception as e:
            logger.error(f'Failed to save detection result: {str(e)}')

        return Response({
            'overall_score': result['overall_score'],
            'classification': result['classification'],
            'classification_label': result['classification_label'],
            'sentences': result['sentences'],
            'word_count': word_count,
        })
