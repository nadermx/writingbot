import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from plagiarism.services import PlagiarismService
import config

logger = logging.getLogger('app')


class PlagiarismPage(View):
    """Plagiarism checker page - shows premium gate for free users."""

    def get(self, request):
        settings = GlobalVars.get_globals(request)

        is_premium = (
            request.user.is_authenticated
            and request.user.is_plan_active
        )

        usage = None
        if is_premium:
            usage = PlagiarismService.check_monthly_usage(request.user)

        return render(
            request,
            'tools/plagiarism.html',
            {
                'title': f"Plagiarism Checker | {config.PROJECT_NAME}",
                'description': 'Check your writing for plagiarism. Scan your text against billions of web pages and get a detailed originality report.',
                'page': 'plagiarism',
                'g': settings,
                'is_premium': is_premium,
                'usage': usage,
            }
        )


class PlagiarismCheckAPI(APIView):
    """POST - Premium only. Validates monthly word limit, runs plagiarism check."""

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Please log in to use the plagiarism checker.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not request.user.is_plan_active:
            return Response(
                {'error': 'The plagiarism checker is a premium feature. Please upgrade your plan.'},
                status=status.HTTP_403_FORBIDDEN
            )

        text = request.data.get('text', '').strip()

        if not text:
            return Response(
                {'error': 'Please provide text to check.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, error = PlagiarismService.check_plagiarism(text, request.user)

        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result)


class PlagiarismUsageAPI(APIView):
    """GET - Returns monthly usage stats."""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Please log in to view usage.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not request.user.is_plan_active:
            return Response(
                {'error': 'The plagiarism checker is a premium feature.'},
                status=status.HTTP_403_FORBIDDEN
            )

        usage = PlagiarismService.check_monthly_usage(request.user)
        return Response(usage)
