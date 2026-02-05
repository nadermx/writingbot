import logging

from django.conf import settings as django_settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from pdf_tools.services import PDFService
import config

logger = logging.getLogger('app')

TOOL_LIMITS = django_settings.TOOL_LIMITS.get('pdf_tools', {})
FREE_DAILY_LIMIT = TOOL_LIMITS.get('free_daily', 3)

# Registry of all PDF tools with metadata
PDF_TOOLS = [
    {
        'slug': 'merge-pdf',
        'name': 'Merge PDF',
        'description': 'Combine multiple PDFs into one document.',
        'icon': 'merge',
        'accepts_multiple': True,
        'accept': '.pdf',
    },
    {
        'slug': 'split-pdf',
        'name': 'Split PDF',
        'description': 'Extract specific pages from a PDF.',
        'icon': 'split',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'pdf-editor',
        'name': 'PDF Editor',
        'description': 'Rotate, reorder, or remove pages from a PDF.',
        'icon': 'edit',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'pdf-to-word',
        'name': 'PDF to Word',
        'description': 'Convert PDF files to editable Word documents.',
        'icon': 'word',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'word-to-pdf',
        'name': 'Word to PDF',
        'description': 'Convert Word documents to PDF format.',
        'icon': 'word',
        'accepts_multiple': False,
        'accept': '.doc,.docx',
    },
    {
        'slug': 'pdf-to-jpg',
        'name': 'PDF to JPG',
        'description': 'Convert PDF pages to JPG images.',
        'icon': 'image',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'jpg-to-pdf',
        'name': 'JPG to PDF',
        'description': 'Convert JPG images to PDF documents.',
        'icon': 'image',
        'accepts_multiple': True,
        'accept': '.jpg,.jpeg',
    },
    {
        'slug': 'pdf-to-png',
        'name': 'PDF to PNG',
        'description': 'Convert PDF pages to PNG images.',
        'icon': 'image',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'png-to-pdf',
        'name': 'PNG to PDF',
        'description': 'Convert PNG images to PDF documents.',
        'icon': 'image',
        'accepts_multiple': True,
        'accept': '.png',
    },
    {
        'slug': 'pdf-to-ppt',
        'name': 'PDF to PowerPoint',
        'description': 'Convert PDF files to PowerPoint presentations.',
        'icon': 'ppt',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'ppt-to-pdf',
        'name': 'PowerPoint to PDF',
        'description': 'Convert PowerPoint files to PDF format.',
        'icon': 'ppt',
        'accepts_multiple': False,
        'accept': '.ppt,.pptx',
    },
    {
        'slug': 'compress-pdf',
        'name': 'Compress PDF',
        'description': 'Reduce PDF file size without losing quality.',
        'icon': 'compress',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'rotate-pdf',
        'name': 'Rotate PDF',
        'description': 'Rotate PDF pages to any angle.',
        'icon': 'rotate',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'remove-pages',
        'name': 'Remove Pages',
        'description': 'Delete unwanted pages from your PDF.',
        'icon': 'delete',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'reorder-pages',
        'name': 'Reorder Pages',
        'description': 'Rearrange the page order in your PDF.',
        'icon': 'reorder',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
    {
        'slug': 'chat-pdf',
        'name': 'Chat with PDF',
        'description': 'Ask questions about your PDF content using AI.',
        'icon': 'chat',
        'accepts_multiple': False,
        'accept': '.pdf',
    },
]

TOOL_MAP = {tool['slug']: tool for tool in PDF_TOOLS}


class PDFToolsIndex(View):
    """Renders the PDF tools index page showing all available tools."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'pdf-tools/index.html', {
            'title': f'Free Online PDF Tools | {config.PROJECT_NAME}',
            'description': 'Free online PDF tools: merge, split, compress, convert, rotate, and more. No installation required.',
            'page': 'pdf-tools',
            'g': g,
            'tools': PDF_TOOLS,
        })


class PDFToolPage(View):
    """Renders individual PDF tool pages."""

    def get(self, request, tool_slug):
        g = GlobalVars.get_globals(request)
        tool = TOOL_MAP.get(tool_slug)
        if not tool:
            return render(request, '404.html', {'g': g}, status=404)

        is_premium = request.user.is_authenticated and request.user.is_plan_active

        return render(request, 'pdf-tools/tool.html', {
            'title': f'{tool["name"]} - Free Online Tool | {config.PROJECT_NAME}',
            'description': tool['description'],
            'page': 'pdf-tools',
            'g': g,
            'tool': tool,
            'is_premium': is_premium,
            'free_daily_limit': FREE_DAILY_LIMIT,
        })


# ---- API Views ----

class PDFMergeAPI(APIView):
    """POST /api/pdf/merge/ - Merge multiple PDF files."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        files = request.FILES.getlist('files')

        if len(files) < 2:
            return Response(
                {'error': 'Please upload at least 2 PDF files to merge.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = PDFService.merge_pdfs(files)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
        return response


class PDFSplitAPI(APIView):
    """POST /api/pdf/split/ - Split a PDF by page selection."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        pages = request.data.get('pages', 'all')

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = PDFService.split_pdf(file, pages)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="split.pdf"'
        return response


class PDFConvertAPI(APIView):
    """POST /api/pdf/convert/ - Convert to/from PDF."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        direction = request.data.get('direction', 'to_pdf')  # 'to_pdf' or 'from_pdf'
        target_format = request.data.get('format', 'docx')

        if not file:
            return Response(
                {'error': 'Please upload a file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if direction == 'to_pdf':
            source_ext = file.name.rsplit('.', 1)[-1] if '.' in file.name else ''
            output, error = PDFService.convert_to_pdf(file, source_ext)
            content_type = 'application/pdf'
            filename = 'converted.pdf'
        else:
            output, error = PDFService.convert_from_pdf(file, target_format)
            content_types = {
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'jpg': 'image/jpeg',
                'png': 'image/png',
            }
            content_type = content_types.get(target_format, 'application/octet-stream')
            # If multi-page images, it's a zip
            if target_format in ('jpg', 'jpeg', 'png'):
                content_type = 'application/zip'
                filename = f'converted.zip'
            else:
                filename = f'converted.{target_format}'

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class PDFCompressAPI(APIView):
    """POST /api/pdf/compress/ - Compress a PDF."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        quality = request.data.get('quality', 'medium')

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        original_size = file.size
        output, error = PDFService.compress_pdf(file, quality)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = output.read()
        compressed_size = len(content)
        savings = round((1 - compressed_size / original_size) * 100, 1) if original_size > 0 else 0

        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="compressed.pdf"'
        response['X-Original-Size'] = str(original_size)
        response['X-Compressed-Size'] = str(compressed_size)
        response['X-Savings-Percent'] = str(savings)
        return response


class PDFRotateAPI(APIView):
    """POST /api/pdf/rotate/ - Rotate PDF pages."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        page = request.data.get('page', 1)
        angle = request.data.get('angle', 90)

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            page = int(page)
            angle = int(angle)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid page number or angle.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = PDFService.rotate_page(file, page, angle)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rotated.pdf"'
        return response


class PDFRemovePagesAPI(APIView):
    """POST /api/pdf/remove-pages/ - Remove pages from PDF."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        pages = request.data.get('pages', '')

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not pages:
            return Response(
                {'error': 'Please specify which pages to remove.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = PDFService.remove_pages(file, pages)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="edited.pdf"'
        return response


class PDFReorderPagesAPI(APIView):
    """POST /api/pdf/reorder/ - Reorder pages in PDF."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        import json

        file = request.FILES.get('file')
        order_str = request.data.get('order', '[]')

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = json.loads(order_str) if isinstance(order_str, str) else order_str
        except (json.JSONDecodeError, TypeError):
            return Response(
                {'error': 'Invalid page order format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = PDFService.reorder_pages(file, order)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reordered.pdf"'
        return response


class PDFInfoAPI(APIView):
    """POST /api/pdf/info/ - Get PDF metadata and page count."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        info, error = PDFService.get_pdf_info(file)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(info)


class ChatPDFAPI(APIView):
    """POST /api/pdf/chat/ - Ask questions about a PDF."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        question = request.data.get('question', '').strip()

        if not file:
            return Response(
                {'error': 'Please upload a PDF file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not question:
            return Response(
                {'error': 'Please enter a question about the PDF.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        answer, error = PDFService.chat_with_pdf(file, question, use_premium=is_premium)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'answer': answer, 'question': question})
