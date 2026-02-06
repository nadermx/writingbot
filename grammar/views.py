import json
import logging
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from accounts.views import GlobalVars
from grammar.models import GrammarCheckHistory
from grammar.services import AIGrammarService, ProofreaderService

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


class ProofreaderPage(View):
    """Render the proofreader tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )
        limits = settings.TOOL_LIMITS.get('proofreader', {})
        free_word_limit = limits.get('free_words', 5000)

        context = {
            'g': g,
            'title': f"Online Proofreader - {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free online proofreader. Upload a document or paste text to get a comprehensive proofreading report with quality score, error breakdown, and corrected text.',
            'page': 'proofreader',
            'is_premium': is_premium,
            'free_word_limit': free_word_limit,
        }
        return render(request, 'tools/proofreader.html', context)


class ProofreadAPI(APIView):
    """
    API endpoint that accepts text or a file upload and returns
    a comprehensive proofreading report.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        service = ProofreaderService()
        text = None

        # Check if a file was uploaded
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Validate file size
            if uploaded_file.size > service.MAX_FILE_SIZE:
                return Response(
                    {'error': 'File is too large. Maximum size is 10 MB.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate extension
            ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else ''
            if ext not in service.ALLOWED_EXTENSIONS:
                return Response(
                    {'error': f'Unsupported file type ".{ext}". Please upload a DOCX, TXT, or PDF file.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            text, error = service.extract_text_from_file(uploaded_file)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Get text from request body
            text = request.data.get('text', '').strip()

        if not text:
            return Response(
                {'error': 'Please provide text or upload a document to proofread.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Word count check
        word_count = len(text.split())
        limits = settings.TOOL_LIMITS.get('proofreader', {})
        free_limit = limits.get('free_words', 5000)
        is_premium = (
            request.user.is_authenticated and
            getattr(request.user, 'is_plan_active', False)
        )

        if not is_premium and word_count > free_limit:
            return Response(
                {
                    'error': f'Free accounts are limited to {free_limit} words. Your document has {word_count} words.',
                    'upgrade': True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        result, error = service.proofread(text, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'overall_score': result.get('overall_score', 0),
            'summary': result.get('summary', ''),
            'error_counts': result.get('error_counts', {}),
            'total_errors': result.get('total_errors', 0),
            'corrections': result.get('corrections', []),
            'corrected_text': result.get('corrected_text', ''),
            'original_text': text,
            'word_count': word_count,
        })


class ProofreadDownloadAPI(APIView):
    """
    API endpoint to download the corrected document as DOCX or TXT.
    """

    def post(self, request):
        corrected_text = request.data.get('corrected_text', '').strip()
        file_format = request.data.get('format', 'docx').lower()

        if not corrected_text:
            return Response(
                {'error': 'No corrected text provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = ProofreaderService()

        if file_format == 'txt':
            output, error = service.generate_corrected_txt(corrected_text)
            if error:
                return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = HttpResponse(
                output.getvalue(),
                content_type='text/plain'
            )
            response['Content-Disposition'] = 'attachment; filename="proofread_document.txt"'
            return response
        else:
            output, error = service.generate_corrected_docx(corrected_text)
            if error:
                return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename="proofread_document.docx"'
            return response
