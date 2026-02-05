import io
import logging
import os
import tempfile

from django.conf import settings

from core.llm_client import LLMClient

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
    def generate_image_prompt(cls, description, use_premium=False):
        """
        Generate a detailed image generation prompt from a user description.
        This returns a refined prompt, not an actual image (since Claude does not generate images).
        The frontend can then use this prompt with a client-side image gen service.

        Args:
            description: User's image description.
            use_premium: If True, use premium LLM model.

        Returns:
            Tuple of (refined_prompt, error).
        """
        if not description or not description.strip():
            return None, 'Please enter an image description.'

        text, error = LLMClient.generate(
            system_prompt=(
                'You are an expert at crafting detailed image generation prompts. '
                'Given a user description, create a detailed, vivid prompt that would produce a high-quality image. '
                'Include details about style, lighting, composition, colors, and mood. '
                'Return ONLY the refined prompt text, nothing else.'
            ),
            messages=[
                {'role': 'user', 'content': description}
            ],
            max_tokens=1024,
            use_premium=use_premium,
        )
        if error:
            return None, error
        return text, None


class TranscriptionService:
    """Service for audio transcription (speech-to-text)."""

    SUPPORTED_AUDIO = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'webm', 'mp4', 'mpeg'}

    @classmethod
    def transcribe(cls, file):
        """
        Transcribe an audio file to text.

        Args:
            file: UploadedFile object containing audio.

        Returns:
            Tuple of (transcription text, error).
        """
        try:
            if not file:
                return None, 'Please upload an audio file.'

            # Validate file extension
            ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
            if ext not in cls.SUPPORTED_AUDIO:
                return None, f'Unsupported audio format: .{ext}. Supported: {", ".join(sorted(cls.SUPPORTED_AUDIO))}'

            # Check file size (max 25MB)
            if file.size > 25 * 1024 * 1024:
                return None, 'File is too large. Maximum 25MB.'

            # Save to temp file for processing
            with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False) as tmp:
                for chunk in file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                # Try using OpenAI Whisper API if available
                try:
                    import openai
                    client = openai.OpenAI(api_key=getattr(settings, 'OPENAI_API_KEY', ''))
                    with open(tmp_path, 'rb') as audio_file:
                        transcript = client.audio.transcriptions.create(
                            model='whisper-1',
                            file=audio_file,
                        )
                    return transcript.text, None
                except (ImportError, Exception):
                    pass

                # Fallback: use Claude to describe what transcription would contain
                # based on file metadata
                import mutagen
                try:
                    audio_info = mutagen.File(tmp_path)
                    duration = audio_info.info.length if audio_info and audio_info.info else 0
                    duration_str = f'{int(duration // 60)}m {int(duration % 60)}s' if duration else 'unknown'
                except Exception:
                    duration_str = 'unknown'

                import anthropic
                client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                response = client.messages.create(
                    model=settings.ANTHROPIC_MODEL,
                    max_tokens=2048,
                    system=(
                        'You are a transcription assistant. The user has uploaded an audio file for transcription. '
                        'Since you cannot directly process audio, explain that the transcription service requires '
                        'the Whisper API integration to be configured. Provide helpful information about the uploaded file.'
                    ),
                    messages=[
                        {'role': 'user', 'content': (
                            f'Audio file uploaded: {file.name}\n'
                            f'Format: {ext.upper()}\n'
                            f'Size: {file.size / 1024:.1f} KB\n'
                            f'Duration: {duration_str}\n\n'
                            'Please provide a status message about this transcription request.'
                        )}
                    ]
                )
                result = response.content[0].text.strip()
                return result, None

            finally:
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f'Transcription failed: {e}')
            return None, 'Failed to transcribe audio. Please try again.'


class LogoService:
    """Service for AI logo generation prompts."""

    STYLES = {
        'modern': 'Modern & Minimalist',
        'vintage': 'Vintage & Retro',
        'playful': 'Playful & Fun',
        'elegant': 'Elegant & Luxurious',
        'bold': 'Bold & Strong',
        'tech': 'Tech & Futuristic',
        'organic': 'Organic & Natural',
        'geometric': 'Geometric & Abstract',
    }

    @classmethod
    def generate_logo_prompt(cls, business_name, industry='', style='modern', colors='', additional='', use_premium=False):
        """
        Generate a detailed logo design description using AI.

        Args:
            business_name: Name of the business.
            industry: Business industry/sector.
            style: Design style from STYLES.
            colors: Preferred color palette.
            additional: Additional preferences or requirements.
            use_premium: If True, use premium LLM model.

        Returns:
            Tuple of (logo design description, error).
        """
        if not business_name or not business_name.strip():
            return None, 'Please enter a business name.'

        style_label = cls.STYLES.get(style, 'Modern & Minimalist')

        text, error = LLMClient.generate(
            system_prompt=(
                'You are an expert logo designer and brand identity consultant. '
                'Given business details, create a comprehensive logo design brief with:\n'
                '1. **Concept**: A clear description of the logo concept and symbolism\n'
                '2. **Typography**: Font style recommendations and text treatment\n'
                '3. **Icon/Symbol**: Detailed description of any icon or graphical element\n'
                '4. **Color Palette**: Specific hex color codes with usage guidelines\n'
                '5. **Variations**: Suggestions for horizontal, stacked, and icon-only versions\n'
                '6. **AI Image Prompt**: A ready-to-use prompt for AI image generators like DALL-E or Midjourney\n\n'
                'Be specific, creative, and professional. Format with clear markdown headings.'
            ),
            messages=[
                {'role': 'user', 'content': (
                    f'Business Name: {business_name}\n'
                    f'Industry: {industry or "Not specified"}\n'
                    f'Style: {style_label}\n'
                    f'Preferred Colors: {colors or "Designer\'s choice"}\n'
                    f'Additional Notes: {additional or "None"}\n\n'
                    'Please create a detailed logo design brief and AI generation prompt.'
                )}
            ],
            max_tokens=1500,
            use_premium=use_premium,
        )
        if error:
            return None, error
        return text, None


class CharacterService:
    """Service for AI character generation."""

    STYLES = {
        'anime': 'Anime / Manga',
        'realistic': 'Photorealistic',
        'cartoon': 'Cartoon',
        'pixel': 'Pixel Art',
        'fantasy': 'Fantasy / RPG',
        'comic': 'Comic Book',
        'chibi': 'Chibi / Cute',
        'concept': 'Concept Art',
    }

    @classmethod
    def generate_character(cls, name='', traits='', style='concept', gender='', age='', additional='', use_premium=False):
        """
        Generate a detailed AI character description.

        Args:
            name: Character name (optional).
            traits: Character personality traits and features.
            style: Art style from STYLES.
            gender: Character gender (optional).
            age: Character age range (optional).
            additional: Additional details.
            use_premium: If True, use premium LLM model.

        Returns:
            Tuple of (character description, error).
        """
        if not traits or not traits.strip():
            return None, 'Please describe your character traits or features.'

        style_label = cls.STYLES.get(style, 'Concept Art')

        text, error = LLMClient.generate(
            system_prompt=(
                'You are an expert character designer for games, animation, and storytelling. '
                'Given character details, create a comprehensive character sheet with:\n'
                '1. **Visual Description**: Detailed physical appearance (hair, eyes, build, distinguishing features)\n'
                '2. **Outfit & Accessories**: Clothing, armor, accessories, and props\n'
                '3. **Personality Profile**: Key traits, motivations, quirks\n'
                '4. **Background**: Brief backstory that informs the design\n'
                '5. **Color Palette**: Key colors associated with the character\n'
                '6. **Pose Suggestions**: 3 recommended poses for illustration\n'
                '7. **AI Image Prompt**: A ready-to-use prompt for AI image generators, '
                'optimized for the specified art style\n\n'
                'Be creative, detailed, and consistent with the requested style. Format with clear markdown headings.'
            ),
            messages=[
                {'role': 'user', 'content': (
                    f'Character Name: {name or "Unnamed"}\n'
                    f'Traits/Description: {traits}\n'
                    f'Art Style: {style_label}\n'
                    f'Gender: {gender or "Not specified"}\n'
                    f'Age: {age or "Not specified"}\n'
                    f'Additional Details: {additional or "None"}\n\n'
                    'Please create a detailed character sheet and AI generation prompt.'
                )}
            ],
            max_tokens=2000,
            use_premium=use_premium,
        )
        if error:
            return None, error
        return text, None


class WordCloudService:
    """Service for word cloud image generation."""

    COLORMAPS = {
        'viridis': 'Viridis (Blue-Green-Yellow)',
        'plasma': 'Plasma (Purple-Orange-Yellow)',
        'inferno': 'Inferno (Black-Red-Yellow)',
        'magma': 'Magma (Black-Purple-Yellow)',
        'cividis': 'Cividis (Blue-Yellow)',
        'Set2': 'Pastel',
        'Dark2': 'Dark',
        'tab10': 'Bold Colors',
        'Paired': 'Paired Colors',
        'coolwarm': 'Cool-Warm (Blue-Red)',
    }

    @staticmethod
    def generate_word_cloud(text, width=800, height=400, bg_color='white', colormap='viridis',
                            max_words=200, min_font_size=10):
        """
        Generate a word cloud image from text.

        Args:
            text: Input text to generate word cloud from.
            width: Image width in pixels.
            height: Image height in pixels.
            bg_color: Background color name or hex.
            colormap: Matplotlib colormap name.
            max_words: Maximum number of words to display.
            min_font_size: Minimum font size.

        Returns:
            Tuple of (BytesIO PNG output, error).
        """
        try:
            from wordcloud import WordCloud
            import io

            if not text or not text.strip():
                return None, 'Please enter some text to generate a word cloud.'

            if len(text) < 10:
                return None, 'Please enter more text (at least 10 characters).'

            # Clamp parameters
            width = max(200, min(2000, int(width)))
            height = max(200, min(2000, int(height)))
            max_words = max(10, min(500, int(max_words)))
            min_font_size = max(4, min(30, int(min_font_size)))

            wc = WordCloud(
                width=width,
                height=height,
                background_color=bg_color,
                colormap=colormap,
                max_words=max_words,
                min_font_size=min_font_size,
                prefer_horizontal=0.7,
                relative_scaling=0.5,
                margin=10,
            )
            wc.generate(text)

            output = io.BytesIO()
            wc.to_image().save(output, format='PNG')
            output.seek(0)
            return output, None

        except ImportError:
            logger.error('wordcloud package is not installed')
            return None, 'Word cloud generation is not available. Please install the wordcloud package.'
        except Exception as e:
            logger.error(f'Word cloud generation failed: {e}')
            return None, 'Failed to generate word cloud. Please try again.'


class BannerService:
    """Service for AI banner design generation."""

    SIZES = {
        '728x90': 'Leaderboard (728x90)',
        '300x250': 'Medium Rectangle (300x250)',
        '336x280': 'Large Rectangle (336x280)',
        '160x600': 'Wide Skyscraper (160x600)',
        '320x50': 'Mobile Banner (320x50)',
        '970x250': 'Billboard (970x250)',
        '1200x628': 'Facebook/LinkedIn (1200x628)',
        '1080x1080': 'Instagram Square (1080x1080)',
        '1080x1920': 'Instagram Story (1080x1920)',
        '1500x500': 'Twitter Header (1500x500)',
    }

    @classmethod
    def generate_banner(cls, title, subtitle='', cta='', size='1200x628', style='', brand_colors='', additional='', use_premium=False):
        """
        Generate a detailed banner design description using AI.

        Args:
            title: Main headline text.
            subtitle: Secondary text.
            cta: Call-to-action text.
            size: Banner size from SIZES.
            style: Design style preference.
            brand_colors: Brand color palette.
            additional: Additional requirements.
            use_premium: If True, use premium LLM model.

        Returns:
            Tuple of (banner design description, error).
        """
        if not title or not title.strip():
            return None, 'Please enter a banner title.'

        size_label = cls.SIZES.get(size, size)
        try:
            width, height = size.split('x')
            orientation = 'horizontal' if int(width) > int(height) else 'vertical' if int(height) > int(width) else 'square'
        except ValueError:
            orientation = 'horizontal'

        text, error = LLMClient.generate(
            system_prompt=(
                'You are an expert digital advertising designer. '
                'Given banner details, create a comprehensive banner design brief with:\n'
                '1. **Layout**: Detailed layout description for the specific dimensions\n'
                '2. **Visual Elements**: Background, images, patterns, and graphical elements\n'
                '3. **Typography**: Font choices, sizes, and hierarchy for the headline, subtitle, and CTA\n'
                '4. **Color Scheme**: Specific hex colors for all elements\n'
                '5. **CTA Button**: Button design, shape, color, and placement\n'
                '6. **Design Tips**: Best practices for the specific ad format\n'
                '7. **AI Image Prompt**: A ready-to-use prompt for AI image generators to create the banner background or full design\n\n'
                'Be specific about positioning, spacing, and proportions for the given dimensions. '
                'Format with clear markdown headings.'
            ),
            messages=[
                {'role': 'user', 'content': (
                    f'Banner Title: {title}\n'
                    f'Subtitle: {subtitle or "None"}\n'
                    f'Call to Action: {cta or "None"}\n'
                    f'Size: {size_label} ({size}px)\n'
                    f'Orientation: {orientation}\n'
                    f'Style: {style or "Professional and clean"}\n'
                    f'Brand Colors: {brand_colors or "Designer\'s choice"}\n'
                    f'Additional Notes: {additional or "None"}\n\n'
                    'Please create a detailed banner design brief and AI generation prompt.'
                )}
            ],
            max_tokens=1500,
            use_premium=use_premium,
        )
        if error:
            return None, error
        return text, None


class PresentationService:
    """Service for AI presentation generation."""

    STYLES = {
        'professional': 'Professional / Corporate',
        'creative': 'Creative / Colorful',
        'minimal': 'Minimal / Clean',
        'academic': 'Academic / Research',
        'pitch': 'Startup Pitch Deck',
        'educational': 'Educational / Training',
        'sales': 'Sales / Marketing',
    }

    @classmethod
    def generate_presentation(cls, topic, num_slides=10, style='professional', audience='', additional='', use_premium=False):
        """
        Generate a detailed presentation outline with slide-by-slide content.

        Args:
            topic: Presentation topic.
            num_slides: Number of slides to generate (5-30).
            style: Presentation style from STYLES.
            audience: Target audience description.
            additional: Additional requirements.
            use_premium: If True, use premium LLM model.

        Returns:
            Tuple of (presentation content, error).
        """
        if not topic or not topic.strip():
            return None, 'Please enter a presentation topic.'

        num_slides = max(3, min(30, int(num_slides)))
        style_label = cls.STYLES.get(style, 'Professional / Corporate')

        text, error = LLMClient.generate(
            system_prompt=(
                'You are an expert presentation designer and content strategist. '
                'Create a complete, slide-by-slide presentation outline. For each slide provide:\n\n'
                '**Slide N: [Title]**\n'
                '- **Layout**: Description of the slide layout (title slide, two-column, image+text, etc.)\n'
                '- **Heading**: The slide heading text\n'
                '- **Content**: Bullet points or body text (concise, presentation-ready)\n'
                '- **Speaker Notes**: Brief notes for the presenter\n'
                '- **Visual Suggestion**: Recommended image, chart, or graphic\n\n'
                'Also include:\n'
                '- **Design Theme**: Color palette, font recommendations, overall visual style\n'
                '- **Key Takeaways**: 3-5 main points the audience should remember\n\n'
                'Make the content engaging, well-structured, and ready to use. '
                'Follow the specified presentation style. Format with clear markdown.'
            ),
            messages=[
                {'role': 'user', 'content': (
                    f'Topic: {topic}\n'
                    f'Number of Slides: {num_slides}\n'
                    f'Style: {style_label}\n'
                    f'Target Audience: {audience or "General"}\n'
                    f'Additional Requirements: {additional or "None"}\n\n'
                    f'Please create a complete {num_slides}-slide presentation.'
                )}
            ],
            max_tokens=4096,
            use_premium=use_premium,
        )
        if error:
            return None, error
        return text, None
