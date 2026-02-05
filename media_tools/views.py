import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from media_tools.services import (
    ImageService, VoiceService, QRService, AIImageService,
    TranscriptionService, LogoService, CharacterService,
    WordCloudService, BannerService, PresentationService,
)
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
    {
        'slug': 'transcription',
        'name': 'Transcription (Speech to Text)',
        'description': 'Upload audio files and extract text using AI-powered transcription.',
        'category': 'audio',
        'icon': 'transcription',
        'url': '/tools/transcription/',
    },
    {
        'slug': 'logo-generator',
        'name': 'AI Logo Generator',
        'description': 'Generate professional logo design concepts and AI prompts for your brand.',
        'category': 'ai',
        'icon': 'logo',
        'url': '/tools/logo-generator/',
    },
    {
        'slug': 'character-generator',
        'name': 'AI Character Generator',
        'description': 'Create detailed character designs with AI for games, stories, and art.',
        'category': 'ai',
        'icon': 'character',
        'url': '/tools/character-generator/',
    },
    {
        'slug': 'word-cloud',
        'name': 'Word Cloud Generator',
        'description': 'Turn any text into a beautiful word cloud image. Free and instant.',
        'category': 'utility',
        'icon': 'wordcloud',
        'url': '/tools/word-cloud/',
    },
    {
        'slug': 'banner-generator',
        'name': 'AI Banner Generator',
        'description': 'Create banner ad designs with AI for social media and display ads.',
        'category': 'ai',
        'icon': 'banner',
        'url': '/tools/banner-generator/',
    },
    {
        'slug': 'presentation-maker',
        'name': 'AI Presentation Maker',
        'description': 'Generate complete slide-by-slide presentations with AI in seconds.',
        'category': 'ai',
        'icon': 'presentation',
        'url': '/tools/presentation-maker/',
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


class TranscriptionPage(View):
    """Transcription (speech-to-text) tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Audio Transcription - Speech to Text | {config.PROJECT_NAME}',
            'description': 'Convert audio files to text with AI-powered transcription. Supports MP3, WAV, OGG, FLAC, and more.',
            'page': 'transcription',
            'g': g,
            'tool_type': 'transcription',
            'tool_name': 'Transcription (Speech to Text)',
            'tool_description': 'Upload an audio file and get an accurate text transcription using AI.',
            'accept': 'audio/*,.mp3,.wav,.ogg,.flac,.m4a,.webm',
        })


class LogoGeneratorPage(View):
    """AI logo generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Logo Generator | {config.PROJECT_NAME}',
            'description': 'Generate professional logo design concepts and AI-ready prompts for your brand identity.',
            'page': 'logo-generator',
            'g': g,
            'tool_type': 'logo-generator',
            'tool_name': 'AI Logo Generator',
            'tool_description': 'Enter your business details and get a detailed logo design brief with AI image generation prompts.',
            'accept': '',
            'logo_styles': LogoService.STYLES,
        })


class CharacterGeneratorPage(View):
    """AI character generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Character Generator | {config.PROJECT_NAME}',
            'description': 'Create detailed character designs with AI for games, stories, animation, and concept art.',
            'page': 'character-generator',
            'g': g,
            'tool_type': 'character-generator',
            'tool_name': 'AI Character Generator',
            'tool_description': 'Describe your character and get a complete character sheet with AI image generation prompts.',
            'accept': '',
            'character_styles': CharacterService.STYLES,
        })


class WordCloudPage(View):
    """Word cloud generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'Free Word Cloud Generator | {config.PROJECT_NAME}',
            'description': 'Create beautiful word cloud images from any text. Free online word cloud maker.',
            'page': 'word-cloud',
            'g': g,
            'tool_type': 'word-cloud',
            'tool_name': 'Word Cloud Generator',
            'tool_description': 'Paste your text and generate a stunning word cloud image instantly.',
            'accept': '',
            'colormaps': WordCloudService.COLORMAPS,
        })


class BannerGeneratorPage(View):
    """AI banner generator tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Banner Generator | {config.PROJECT_NAME}',
            'description': 'Generate professional banner ad designs with AI for social media and display advertising.',
            'page': 'banner-generator',
            'g': g,
            'tool_type': 'banner-generator',
            'tool_name': 'AI Banner Generator',
            'tool_description': 'Enter your banner details and get a complete design brief with AI image generation prompts.',
            'accept': '',
            'banner_sizes': BannerService.SIZES,
        })


class PresentationMakerPage(View):
    """AI presentation maker tool page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'media-tools/tool.html', {
            'title': f'AI Presentation Maker | {config.PROJECT_NAME}',
            'description': 'Generate complete slide-by-slide presentations with AI. Free online presentation creator.',
            'page': 'presentation-maker',
            'g': g,
            'tool_type': 'presentation-maker',
            'tool_name': 'AI Presentation Maker',
            'tool_description': 'Enter your topic and get a complete presentation with slide content, speaker notes, and visual suggestions.',
            'accept': '',
            'presentation_styles': PresentationService.STYLES,
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

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        prompt, error = AIImageService.generate_image_prompt(description, use_premium=is_premium)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'prompt': prompt})


class TranscribeAPI(APIView):
    """POST /api/media/transcribe/ - Transcribe audio to text."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'Please upload an audio file.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, error = TranscriptionService.transcribe(file)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class LogoGenerateAPI(APIView):
    """POST /api/media/logo/ - Generate logo design prompt."""

    def post(self, request):
        business_name = request.data.get('business_name', '').strip()
        industry = request.data.get('industry', '').strip()
        style = request.data.get('style', 'modern')
        colors = request.data.get('colors', '').strip()
        additional = request.data.get('additional', '').strip()

        if not business_name:
            return Response(
                {'error': 'Please enter a business name.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = LogoService.generate_logo_prompt(
            business_name, industry, style, colors, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class CharacterGenerateAPI(APIView):
    """POST /api/media/character/ - Generate character description."""

    def post(self, request):
        name = request.data.get('name', '').strip()
        traits = request.data.get('traits', '').strip()
        style = request.data.get('style', 'concept')
        gender = request.data.get('gender', '').strip()
        age = request.data.get('age', '').strip()
        additional = request.data.get('additional', '').strip()

        if not traits:
            return Response(
                {'error': 'Please describe your character traits or features.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = CharacterService.generate_character(
            name, traits, style, gender, age, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class WordCloudAPI(APIView):
    """POST /api/media/word-cloud/ - Generate word cloud image."""

    def post(self, request):
        text = request.data.get('text', '').strip()
        width = int(request.data.get('width', 800))
        height = int(request.data.get('height', 400))
        bg_color = request.data.get('bg_color', 'white')
        colormap = request.data.get('colormap', 'viridis')
        max_words = int(request.data.get('max_words', 200))

        if not text:
            return Response(
                {'error': 'Please enter some text.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        output, error = WordCloudService.generate_word_cloud(
            text, width, height, bg_color, colormap, max_words
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = HttpResponse(output.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="wordcloud.png"'
        return response


class BannerGenerateAPI(APIView):
    """POST /api/media/banner/ - Generate banner design prompt."""

    def post(self, request):
        title = request.data.get('title', '').strip()
        subtitle = request.data.get('subtitle', '').strip()
        cta = request.data.get('cta', '').strip()
        size = request.data.get('size', '1200x628')
        style = request.data.get('style', '').strip()
        brand_colors = request.data.get('brand_colors', '').strip()
        additional = request.data.get('additional', '').strip()

        if not title:
            return Response(
                {'error': 'Please enter a banner title.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = BannerService.generate_banner(
            title, subtitle, cta, size, style, brand_colors, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})


class PresentationGenerateAPI(APIView):
    """POST /api/media/presentation/ - Generate presentation content."""

    def post(self, request):
        topic = request.data.get('topic', '').strip()
        num_slides = int(request.data.get('num_slides', 10))
        style = request.data.get('style', 'professional')
        audience = request.data.get('audience', '').strip()
        additional = request.data.get('additional', '').strip()

        if not topic:
            return Response(
                {'error': 'Please enter a presentation topic.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = PresentationService.generate_presentation(
            topic, num_slides, style, audience, additional, use_premium=is_premium
        )
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'result': result})
