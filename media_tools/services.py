import io
import logging
import os
import tempfile

import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class ImageService:
    """Service for image conversion and background removal."""

    SUPPORTED_FORMATS = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG',
        'gif': 'GIF',
        'bmp': 'BMP',
        'webp': 'WEBP',
        'tiff': 'TIFF',
        'ico': 'ICO',
    }

    @classmethod
    def convert(cls, file, target_format, quality=90):
        """
        Convert an image file to a different format.

        Args:
            file: UploadedFile object.
            target_format: Target format string (e.g. 'png', 'jpg').
            quality: JPEG quality 1-100.

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from PIL import Image

            target_format = target_format.lower().strip('.')
            pil_format = cls.SUPPORTED_FORMATS.get(target_format)
            if not pil_format:
                return None, f'Unsupported target format: {target_format}'

            img = Image.open(file)

            # Handle transparency for JPEG
            if pil_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                img = background
            elif pil_format != 'JPEG' and img.mode == 'CMYK':
                img = img.convert('RGB')

            output = io.BytesIO()
            save_kwargs = {}
            if pil_format == 'JPEG':
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif pil_format == 'PNG':
                save_kwargs['optimize'] = True
            elif pil_format == 'WEBP':
                save_kwargs['quality'] = quality

            img.save(output, pil_format, **save_kwargs)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'Image conversion failed: {e}')
            return None, 'Failed to convert image. Please ensure the file is a valid image.'

    @classmethod
    def remove_background(cls, file):
        """
        Remove the background from an image using rembg.

        Args:
            file: UploadedFile object.

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from rembg import remove
            from PIL import Image

            img = Image.open(file)
            result = remove(img)

            output = io.BytesIO()
            result.save(output, 'PNG')
            output.seek(0)
            return output, None

        except ImportError:
            logger.error('rembg is not installed for background removal')
            return None, 'Background removal is not available. Please install the rembg package.'
        except Exception as e:
            logger.error(f'Background removal failed: {e}')
            return None, 'Failed to remove background. Please try a different image.'

    @classmethod
    def resize(cls, file, width=None, height=None, maintain_aspect=True):
        """
        Resize an image.

        Args:
            file: UploadedFile object.
            width: Target width (int or None).
            height: Target height (int or None).
            maintain_aspect: Keep aspect ratio.

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from PIL import Image

            img = Image.open(file)
            original_format = img.format or 'PNG'

            if width and height and not maintain_aspect:
                img = img.resize((width, height), Image.LANCZOS)
            elif width or height:
                if maintain_aspect:
                    img.thumbnail((width or 99999, height or 99999), Image.LANCZOS)
                else:
                    new_w = width or img.width
                    new_h = height or img.height
                    img = img.resize((new_w, new_h), Image.LANCZOS)

            output = io.BytesIO()
            img.save(output, original_format)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'Image resize failed: {e}')
            return None, 'Failed to resize image.'


class VoiceService:
    """Service for text-to-speech generation using external APIs."""

    VOICES = {
        'alloy': 'Alloy - Neutral and balanced',
        'echo': 'Echo - Warm and clear',
        'fable': 'Fable - British accent',
        'onyx': 'Onyx - Deep and authoritative',
        'nova': 'Nova - Friendly and upbeat',
        'shimmer': 'Shimmer - Soft and gentle',
    }

    @classmethod
    def text_to_speech(cls, text, voice='alloy', speed=1.0):
        """
        Convert text to speech audio.

        Args:
            text: The text to convert.
            voice: Voice ID string.
            speed: Playback speed multiplier (0.5-2.0).

        Returns:
            Tuple of (BytesIO audio output, error).
        """
        try:
            if not text or not text.strip():
                return None, 'Please enter some text to convert.'

            if len(text) > 5000:
                return None, 'Text is too long. Maximum 5,000 characters.'

            if voice not in cls.VOICES:
                voice = 'alloy'

            speed = max(0.5, min(2.0, float(speed)))

            # Use edge-tts as a free TTS engine
            import edge_tts
            import asyncio

            voice_map = {
                'alloy': 'en-US-JennyNeural',
                'echo': 'en-US-GuyNeural',
                'fable': 'en-GB-SoniaNeural',
                'onyx': 'en-US-DavisNeural',
                'nova': 'en-US-AriaNeural',
                'shimmer': 'en-US-AnaNeural',
            }

            edge_voice = voice_map.get(voice, 'en-US-JennyNeural')
            rate_str = f'+{int((speed - 1) * 100)}%' if speed >= 1 else f'{int((speed - 1) * 100)}%'

            output = io.BytesIO()

            async def _generate():
                communicate = edge_tts.Communicate(text, edge_voice, rate=rate_str)
                async for chunk in communicate.stream():
                    if chunk['type'] == 'audio':
                        output.write(chunk['data'])

            asyncio.run(_generate())
            output.seek(0)

            if output.getbuffer().nbytes == 0:
                return None, 'Failed to generate audio. Please try again.'

            return output, None

        except ImportError:
            logger.error('edge-tts is not installed for voice generation')
            return None, 'Voice generation is not available. Please install the edge-tts package.'
        except Exception as e:
            logger.error(f'Text-to-speech failed: {e}')
            return None, 'Failed to generate voice audio. Please try again.'


class QRService:
    """Service for QR code generation."""

    @classmethod
    def generate_qr(cls, data, size=300, color='#000000', bg_color='#FFFFFF', error_correction='M'):
        """
        Generate a QR code image.

        Args:
            data: The content to encode in the QR code.
            size: Image size in pixels.
            color: Foreground color hex.
            bg_color: Background color hex.
            error_correction: Error correction level (L, M, Q, H).

        Returns:
            Tuple of (BytesIO image output, error).
        """
        try:
            import qrcode
            from qrcode.constants import (
                ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
            )

            if not data or not data.strip():
                return None, 'Please enter data to encode.'

            ec_map = {
                'L': ERROR_CORRECT_L,
                'M': ERROR_CORRECT_M,
                'Q': ERROR_CORRECT_Q,
                'H': ERROR_CORRECT_H,
            }

            qr = qrcode.QRCode(
                version=None,  # Auto-detect
                error_correction=ec_map.get(error_correction.upper(), ERROR_CORRECT_M),
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color=color, back_color=bg_color)

            # Resize to requested size
            from PIL import Image
            img = img.resize((size, size), Image.LANCZOS)

            output = io.BytesIO()
            img.save(output, 'PNG')
            output.seek(0)
            return output, None

        except ImportError:
            logger.error('qrcode package is not installed')
            return None, 'QR code generation is not available. Please install the qrcode package.'
        except Exception as e:
            logger.error(f'QR code generation failed: {e}')
            return None, 'Failed to generate QR code.'


class AIImageService:
    """Service for AI image generation using Anthropic Claude."""

    @classmethod
    def generate_image_prompt(cls, description):
        """
        Generate a detailed image generation prompt from a user description.
        This returns a refined prompt, not an actual image (since Claude does not generate images).
        The frontend can then use this prompt with a client-side image gen service.

        Args:
            description: User's image description.

        Returns:
            Tuple of (refined_prompt, error).
        """
        try:
            if not description or not description.strip():
                return None, 'Please enter an image description.'

            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=1024,
                system=(
                    'You are an expert at crafting detailed image generation prompts. '
                    'Given a user description, create a detailed, vivid prompt that would produce a high-quality image. '
                    'Include details about style, lighting, composition, colors, and mood. '
                    'Return ONLY the refined prompt text, nothing else.'
                ),
                messages=[
                    {'role': 'user', 'content': description}
                ]
            )
            refined = response.content[0].text.strip()
            return refined, None

        except anthropic.RateLimitError:
            return None, 'Service is temporarily busy. Please try again.'
        except Exception as e:
            logger.error(f'AI image prompt generation failed: {e}')
            return None, 'Failed to generate image prompt.'
