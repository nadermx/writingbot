import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from media_tools.services import ImageService, VoiceService, QRService, AIImageService
import config

logger = logging.getLogger('app')

# Registry of all media tools
MEDIA_TOOLS = [
    {
        'slug': 'image-converter',
        'name': 'Image Converter',
        'description': 'Convert images between JPG, PNG, WebP, GIF, BMP, and more.',
        'category': 'image',
        'icon': 'image',
        'url': '/image-tools/',
    },
    {
        'slug': 'background-remover',
        'name': 'Background Remover',
        'description': 'Remove backgrounds from images instantly with AI.',
        'category': 'image',
        'icon': 'bg-remove',
        'url': '/background-remover/',
    },
    {
        'slug': 'ai-image-generator',
        'name': 'AI Image Generator',
        'description': 'Generate image prompts with AI to create stunning visuals.',
        'category': 'ai',
        'icon': 'ai',
        'url': '/converter-tools/',
    },
    {
        'slug': 'qr-code-generator',
        'name': 'QR Code Generator',
        'description': 'Create custom QR codes for URLs, text, and more.',
        'category': 'utility',
        'icon': 'qr',
        'url': '/tools/qr-code-generator/',
    },
    {
        'slug': 'ai-voice-generator',
        'name': 'AI Voice Generator',
        'description': 'Convert text to natural-sounding speech with multiple voices.',
        'category': 'audio',
        'icon': 'voice',
        'url': '/tools/ai-voice-generator/',
    },
]


class MediaToolsIndex(View):
    """Renders the media tools index page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/index.html', {
            'title': f'Free Online Media Tools | {config.PROJECT_NAME}',
            'description': 'Free online image converter, background remover, QR code generator, and AI voice tools.',
            'page': 'media-tools',
            'g': g,
            'tools': MEDIA_TOOLS,
        })


class ImageConverterPage(View):
    """Image converter tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Image Converter | {config.PROJECT_NAME}',
            'description': 'Convert images between JPG, PNG, WebP, GIF, BMP, TIFF, and ICO. Free online tool, no installation required.',
            'page': 'image-converter',
            'g': g,
            'tool_type': 'image-converter',
            'tool_name': 'Image Converter',
            'tool_description': 'Convert your images to any format. Supports JPG, PNG, WebP, GIF, BMP, TIFF, and ICO.',
            'accept': 'image/*',
            'formats': list(ImageService.SUPPORTED_FORMATS.keys()),
        })


class BackgroundRemoverPage(View):
    """Background remover tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Background Remover | {config.PROJECT_NAME}',
            'description': 'Remove backgrounds from images instantly using AI. Free online tool.',
            'page': 'background-remover',
            'g': g,
            'tool_type': 'background-remover',
            'tool_name': 'Background Remover',
            'tool_description': 'Upload an image and instantly remove its background using AI.',
            'accept': 'image/*',
        })


class AIImageGeneratorPage(View):
    """AI image prompt generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Image Generator | {config.PROJECT_NAME}',
            'description': 'Generate detailed AI image prompts from simple descriptions.',
            'page': 'ai-image-generator',
            'g': g,
            'tool_type': 'ai-image-generator',
            'tool_name': 'AI Image Generator',
            'tool_description': 'Describe what you want and get a detailed, optimized prompt for AI image generation.',
            'accept': '',
        })


class QRCodePage(View):
    """QR code generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free QR Code Generator | {config.PROJECT_NAME}',
            'description': 'Create custom QR codes for URLs, text, WiFi, and more. Free online QR code maker.',
            'page': 'qr-code-generator',
            'g': g,
            'tool_type': 'qr-code',
            'tool_name': 'QR Code Generator',
            'tool_description': 'Generate custom QR codes with your choice of colors and error correction level.',
            'accept': '',
        })


class VoiceGeneratorPage(View):
    """AI voice generator page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Voice Generator - Text to Speech | {config.PROJECT_NAME}',
            'description': 'Convert text to natural-sounding speech. Choose from 6 AI voices. Free online text-to-speech.',
            'page': 'ai-voice-generator',
            'g': g,
            'tool_type': 'voice-generator',
            'tool_name': 'AI Voice Generator',
            'tool_description': 'Convert text to natural-sounding speech with multiple AI voices.',
            'accept': '',
            'voices': VoiceService.VOICES,
        })


# ---- API Views ----

class ImageConvertAPI(APIView):
    """POST /api/media/convert-image/ - Convert image format."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        target_format = request.data.get('format', 'png')
        quality = int(request.data.get('quality', 90))

        if not file:
            return Response(
                {'error': 'Please upload an image file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = ImageService.convert(file, target_format, quality)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content_types = {
            'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
            'gif': 'image/gif', 'bmp': 'image/bmp', 'webp': 'image/webp',
            'tiff': 'image/tiff', 'ico': 'image/x-icon',
        }
        ct = content_types.get(target_format.lower(), 'application/octet-stream')

        response = HttpResponse(output.read(), content_type=ct)
        response['Content-Disposition'] = f'attachment; filename="converted.{target_format}"'
        return response


class BackgroundRemoveAPI(APIView):
    """POST /api/media/remove-bg/ - Remove image background."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'Please upload an image file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = ImageService.remove_background(file)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="no-background.png"'
        return response


class QRCodeAPI(APIView):
    """POST /api/media/qr-code/ - Generate QR code."""

    def post(self, request):
        data = request.data.get('data', '').strip()
        size = int(request.data.get('size', 300))
        color = request.data.get('color', '#000000')
        bg_color = request.data.get('bg_color', '#FFFFFF')
        error_correction = request.data.get('error_correction', 'M')

        if not data:
            return Response(
                {'error': 'Please enter data to encode.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = QRService.generate_qr(data, size, color, bg_color, error_correction)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response


class VoiceGenerateAPI(APIView):
    """POST /api/media/text-to-speech/ - Generate speech audio."""

    def post(self, request):
        text = request.data.get('text', '').strip()
        voice = request.data.get('voice', 'alloy')
        speed = float(request.data.get('speed', 1.0))

        if not text:
            return Response(
                {'error': 'Please enter some text to convert.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = VoiceService.text_to_speech(text, voice, speed)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
        return response


class AIImagePromptAPI(APIView):
    """POST /api/media/ai-image/ - Generate AI image prompt."""

    def post(self, request):
        description = request.data.get('description', '').strip()

        if not description:
            return Response(
                {'error': 'Please enter an image description.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        prompt, error = AIImageService.generate_image_prompt(description)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'prompt': prompt})
