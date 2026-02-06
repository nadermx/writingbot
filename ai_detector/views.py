import io
import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

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
            'classification_description': result.get('classification_description', ''),
            'category_confidences': result.get('category_confidences', {}),
            'sentences': result['sentences'],
            'word_count': word_count,
        })


class AIDetectBulkAPI(APIView):
    """Bulk file upload endpoint for AI detection. Premium only."""
    parser_classes = [MultiPartParser, FormParser]

    MAX_FILES = 10
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB per file
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}

    def post(self, request):
        # Premium check
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        if not is_premium:
            return Response(
                {
                    'error': 'Bulk analysis is available for Premium users only.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN
            )

        files = request.FILES.getlist('files')
        if not files:
            return Response(
                {'error': 'Please upload at least one file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(files) > self.MAX_FILES:
            return Response(
                {'error': f'Maximum {self.MAX_FILES} files allowed per batch.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        errors = []

        for uploaded_file in files:
            filename = uploaded_file.name
            ext = self._get_extension(filename)

            # Validate extension
            if ext not in self.ALLOWED_EXTENSIONS:
                errors.append({
                    'filename': filename,
                    'error': f'Unsupported file type. Allowed: TXT, PDF, DOCX'
                })
                continue

            # Validate file size
            if uploaded_file.size > self.MAX_FILE_SIZE:
                errors.append({
                    'filename': filename,
                    'error': f'File too large. Maximum 5 MB per file.'
                })
                continue

            # Extract text
            try:
                text = self._extract_text(uploaded_file, ext)
            except Exception as e:
                logger.error(f'Text extraction error for {filename}: {str(e)}')
                errors.append({
                    'filename': filename,
                    'error': f'Could not extract text from file.'
                })
                continue

            if not text or not text.strip():
                errors.append({
                    'filename': filename,
                    'error': 'No text content found in file.'
                })
                continue

            word_count = len(text.split())
            if word_count < 80:
                errors.append({
                    'filename': filename,
                    'error': f'Text too short ({word_count} words, minimum 80).'
                })
                continue

            # Run detection
            result, error = AIDetectorService.detect(text, use_premium=is_premium)

            if error:
                errors.append({
                    'filename': filename,
                    'error': error
                })
                continue

            # Save result
            try:
                DetectionResult.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    input_text=text[:5000],  # Truncate for storage
                    results={'sentences': result['sentences']},
                    overall_score=result['overall_score'],
                    classification=result['classification'],
                    word_count=word_count,
                )
            except Exception as e:
                logger.error(f'Failed to save bulk detection result: {str(e)}')

            results.append({
                'filename': filename,
                'word_count': word_count,
                'overall_score': result['overall_score'],
                'classification': result['classification'],
                'classification_label': result['classification_label'],
                'category_confidences': result.get('category_confidences', {}),
            })

        return Response({
            'results': results,
            'errors': errors,
            'total_files': len(files),
            'successful': len(results),
            'failed': len(errors),
        })

    def _get_extension(self, filename):
        """Get lowercase file extension."""
        import os
        _, ext = os.path.splitext(filename)
        return ext.lower()

    def _extract_text(self, uploaded_file, ext):
        """Extract text content from uploaded file."""
        if ext == '.txt':
            return self._extract_txt(uploaded_file)
        elif ext == '.pdf':
            return self._extract_pdf(uploaded_file)
        elif ext == '.docx':
            return self._extract_docx(uploaded_file)
        return ''

    def _extract_txt(self, uploaded_file):
        """Extract text from a .txt file."""
        content = uploaded_file.read()
        # Try UTF-8 first, then fall back to latin-1
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('latin-1')

    def _extract_pdf(self, uploaded_file):
        """Extract text from a PDF file using pdfplumber."""
        import pdfplumber
        content = uploaded_file.read()
        text_parts = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n'.join(text_parts)

    def _extract_docx(self, uploaded_file):
        """Extract text from a .docx file using zipfile + XML parsing."""
        import zipfile
        import xml.etree.ElementTree as ET

        content = uploaded_file.read()
        text_parts = []

        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            # Read the main document content
            if 'word/document.xml' in zf.namelist():
                with zf.open('word/document.xml') as doc_xml:
                    tree = ET.parse(doc_xml)
                    root = tree.getroot()

                    # Word XML namespace
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                    # Extract text from all paragraphs
                    for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                        para_texts = []
                        for run in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                            if run.text:
                                para_texts.append(run.text)
                        if para_texts:
                            text_parts.append(''.join(para_texts))

        return '\n'.join(text_parts)
