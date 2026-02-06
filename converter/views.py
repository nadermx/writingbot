import logging

from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from accounts.views import GlobalVars
import config

logger = logging.getLogger('app')

# =============================================================================
# Format Registries
# =============================================================================

IMAGE_FORMATS = {
    'jpg': {
        'name': 'JPG',
        'extension': '.jpg',
        'full_name': 'JPEG Image',
        'mime': 'image/jpeg',
        'description': 'JPG (JPEG) is the most widely used image format for photographs and web images. It uses lossy compression to achieve small file sizes while maintaining good visual quality.',
        'category': 'image',
    },
    'png': {
        'name': 'PNG',
        'extension': '.png',
        'full_name': 'PNG Image',
        'mime': 'image/png',
        'description': 'PNG (Portable Network Graphics) is a lossless image format that supports transparency. It is ideal for graphics, logos, screenshots, and images that require crisp edges.',
        'category': 'image',
    },
    'webp': {
        'name': 'WebP',
        'extension': '.webp',
        'full_name': 'WebP Image',
        'mime': 'image/webp',
        'description': 'WebP is a modern image format developed by Google that provides superior compression for web images. It supports both lossy and lossless compression, plus transparency.',
        'category': 'image',
    },
    'gif': {
        'name': 'GIF',
        'extension': '.gif',
        'full_name': 'GIF Image',
        'mime': 'image/gif',
        'description': 'GIF (Graphics Interchange Format) supports animation and transparency. It uses lossless compression but is limited to 256 colors, making it ideal for simple graphics and animations.',
        'category': 'image',
    },
    'bmp': {
        'name': 'BMP',
        'extension': '.bmp',
        'full_name': 'BMP Image',
        'mime': 'image/bmp',
        'description': 'BMP (Bitmap) is an uncompressed image format that stores pixel data directly. It produces large files but preserves every detail of the original image without any quality loss.',
        'category': 'image',
    },
    'tiff': {
        'name': 'TIFF',
        'extension': '.tiff',
        'full_name': 'TIFF Image',
        'mime': 'image/tiff',
        'description': 'TIFF (Tagged Image File Format) is a flexible, high-quality image format commonly used in photography, publishing, and archiving. It supports lossless compression and multiple layers.',
        'category': 'image',
    },
    'ico': {
        'name': 'ICO',
        'extension': '.ico',
        'full_name': 'ICO Icon',
        'mime': 'image/x-icon',
        'description': 'ICO is the standard icon format for Windows applications and website favicons. It can contain multiple image sizes and color depths within a single file.',
        'category': 'image',
    },
    'svg': {
        'name': 'SVG',
        'extension': '.svg',
        'full_name': 'SVG Vector',
        'mime': 'image/svg+xml',
        'description': 'SVG (Scalable Vector Graphics) is a vector image format that uses XML markup. It can scale to any size without losing quality, making it perfect for logos, icons, and illustrations.',
        'category': 'image',
    },
    'heic': {
        'name': 'HEIC',
        'extension': '.heic',
        'full_name': 'HEIC Image',
        'mime': 'image/heic',
        'description': 'HEIC (High Efficiency Image Container) is the default photo format on Apple devices. It provides better compression than JPEG while maintaining higher image quality.',
        'category': 'image',
    },
    'avif': {
        'name': 'AVIF',
        'extension': '.avif',
        'full_name': 'AVIF Image',
        'mime': 'image/avif',
        'description': 'AVIF (AV1 Image File Format) is a next-generation image format that offers significantly better compression than JPEG and WebP while maintaining excellent visual quality.',
        'category': 'image',
    },
}

DOCUMENT_FORMATS = {
    'pdf': {
        'name': 'PDF',
        'extension': '.pdf',
        'full_name': 'PDF Document',
        'mime': 'application/pdf',
        'description': 'PDF (Portable Document Format) preserves document formatting across all devices and platforms. It is the standard for sharing documents, forms, and publications.',
        'category': 'document',
    },
    'word': {
        'name': 'Word',
        'extension': '.docx',
        'full_name': 'Microsoft Word Document',
        'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'description': 'Microsoft Word (DOCX) is the most popular word processing format for creating and editing documents, letters, reports, and academic papers.',
        'category': 'document',
    },
    'excel': {
        'name': 'Excel',
        'extension': '.xlsx',
        'full_name': 'Microsoft Excel Spreadsheet',
        'mime': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'description': 'Microsoft Excel (XLSX) is the standard spreadsheet format for data analysis, financial modeling, and tabular data storage.',
        'category': 'document',
    },
    'ppt': {
        'name': 'PowerPoint',
        'extension': '.pptx',
        'full_name': 'Microsoft PowerPoint Presentation',
        'mime': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'description': 'Microsoft PowerPoint (PPTX) is the leading format for creating slide presentations for business, education, and conferences.',
        'category': 'document',
    },
    'csv': {
        'name': 'CSV',
        'extension': '.csv',
        'full_name': 'CSV File',
        'mime': 'text/csv',
        'description': 'CSV (Comma-Separated Values) is a simple text format for tabular data. It is universally supported and commonly used for data exchange between applications.',
        'category': 'document',
    },
    'txt': {
        'name': 'TXT',
        'extension': '.txt',
        'full_name': 'Plain Text File',
        'mime': 'text/plain',
        'description': 'TXT (Plain Text) is the simplest document format containing only unformatted text. It is universally compatible with all operating systems and text editors.',
        'category': 'document',
    },
    'html': {
        'name': 'HTML',
        'extension': '.html',
        'full_name': 'HTML File',
        'mime': 'text/html',
        'description': 'HTML (HyperText Markup Language) is the standard format for web pages. It structures content with tags for headings, paragraphs, links, images, and more.',
        'category': 'document',
    },
    'odt': {
        'name': 'ODT',
        'extension': '.odt',
        'full_name': 'OpenDocument Text',
        'mime': 'application/vnd.oasis.opendocument.text',
        'description': 'ODT (OpenDocument Text) is an open-standard document format used by LibreOffice and OpenOffice. It provides full word processing capabilities without vendor lock-in.',
        'category': 'document',
    },
    'rtf': {
        'name': 'RTF',
        'extension': '.rtf',
        'full_name': 'Rich Text Format',
        'mime': 'application/rtf',
        'description': 'RTF (Rich Text Format) is a cross-platform document format that supports basic formatting like fonts, colors, and alignment while maintaining broad compatibility.',
        'category': 'document',
    },
    'epub': {
        'name': 'EPUB',
        'extension': '.epub',
        'full_name': 'EPUB eBook',
        'mime': 'application/epub+zip',
        'description': 'EPUB (Electronic Publication) is the standard eBook format supported by most e-readers and reading apps. It supports reflowable content that adapts to different screen sizes.',
        'category': 'document',
    },
}

# Combined lookup for all formats
ALL_FORMATS = {**IMAGE_FORMATS, **DOCUMENT_FORMATS}

# =============================================================================
# Conversion type classification
# =============================================================================

def get_conversion_type(source_key, target_key):
    """Return the conversion category type."""
    src = ALL_FORMATS.get(source_key, {})
    tgt = ALL_FORMATS.get(target_key, {})
    src_cat = src.get('category', '')
    tgt_cat = tgt.get('category', '')

    if src_cat == 'image' and tgt_cat == 'image':
        return 'image-to-image'
    elif src_cat == 'document' and tgt_cat == 'document':
        return 'document-to-document'
    elif src_cat == 'image' and tgt_cat == 'document':
        return 'image-to-document'
    elif src_cat == 'document' and tgt_cat == 'image':
        return 'document-to-image'
    return 'other'


def get_api_config(source_key, target_key, conv_type):
    """
    Return the API endpoint and parameters for the given conversion.
    Maps conversion pairs to the existing ImageConvertAPI and PDFConvertAPI.
    """
    src = ALL_FORMATS.get(source_key, {})
    tgt = ALL_FORMATS.get(target_key, {})

    if conv_type == 'image-to-image':
        return {
            'endpoint': '/api/media/convert-image/',
            'method': 'image',
            'accept': 'image/*',
            'target_format': target_key if target_key != 'jpg' else 'jpg',
        }

    # Document conversions involving PDF
    if source_key == 'pdf' or target_key == 'pdf':
        if target_key == 'pdf':
            # Something to PDF
            accept_map = {
                'word': '.doc,.docx',
                'excel': '.xls,.xlsx',
                'ppt': '.ppt,.pptx',
                'jpg': '.jpg,.jpeg',
                'png': '.png',
                'csv': '.csv',
                'txt': '.txt',
                'html': '.html,.htm',
                'odt': '.odt',
                'rtf': '.rtf',
                'epub': '.epub',
            }
            return {
                'endpoint': '/api/pdf/convert/',
                'method': 'pdf',
                'direction': 'to_pdf',
                'accept': accept_map.get(source_key, '*'),
                'target_format': 'pdf',
            }
        else:
            # PDF to something
            format_map = {
                'word': 'docx',
                'excel': 'xlsx',
                'ppt': 'pptx',
                'jpg': 'jpg',
                'png': 'png',
                'csv': 'csv',
                'txt': 'txt',
                'html': 'html',
                'odt': 'odt',
                'rtf': 'rtf',
                'epub': 'epub',
            }
            return {
                'endpoint': '/api/pdf/convert/',
                'method': 'pdf',
                'direction': 'from_pdf',
                'accept': '.pdf',
                'target_format': format_map.get(target_key, target_key),
            }

    # Non-PDF document conversions (e.g., Word to TXT, Excel to CSV)
    # Route to the to_pdf endpoint - the SEO page explains the conversion
    # The UI converts the source to PDF as the primary conversion step
    accept_map = {
        'word': '.doc,.docx',
        'excel': '.xls,.xlsx',
        'ppt': '.ppt,.pptx',
        'csv': '.csv',
        'txt': '.txt',
        'html': '.html,.htm',
        'odt': '.odt',
        'rtf': '.rtf',
        'epub': '.epub',
    }
    return {
        'endpoint': '/api/pdf/convert/',
        'method': 'pdf',
        'direction': 'to_pdf',
        'accept': accept_map.get(source_key, src.get('extension', '*')),
        'target_format': 'pdf',
        'is_cross_doc': True,
    }


def get_accept_string(source_key, conv_type, api_config):
    """Return the file accept attribute for the upload input."""
    return api_config.get('accept', '*')


# =============================================================================
# Generate all valid conversion pairs
# =============================================================================

def get_all_image_pairs():
    """Generate all valid image-to-image conversion pairs."""
    pairs = []
    image_keys = list(IMAGE_FORMATS.keys())
    for src in image_keys:
        for tgt in image_keys:
            if src != tgt:
                pairs.append((src, tgt))
    return pairs


def get_all_document_pairs():
    """Generate all valid document conversion pairs involving PDF and cross-document."""
    pairs = []
    seen = set()
    doc_keys = [k for k in DOCUMENT_FORMATS.keys() if k != 'pdf']

    # Each doc format to/from PDF
    for k in doc_keys:
        pairs.append((k, 'pdf'))
        pairs.append(('pdf', k))
        seen.add((k, 'pdf'))
        seen.add(('pdf', k))

    # Image to/from PDF (for JPG and PNG)
    for img_key in ['jpg', 'png']:
        pair_to = (img_key, 'pdf')
        pair_from = ('pdf', img_key)
        if pair_to not in seen:
            pairs.append(pair_to)
            seen.add(pair_to)
        if pair_from not in seen:
            pairs.append(pair_from)
            seen.add(pair_from)

    # Cross-document conversions (route through PDF as intermediate)
    # These are common conversions people search for
    cross_doc_pairs = [
        ('word', 'txt'), ('txt', 'word'),
        ('word', 'html'), ('html', 'word'),
        ('word', 'rtf'), ('rtf', 'word'),
        ('word', 'odt'), ('odt', 'word'),
        ('excel', 'csv'), ('csv', 'excel'),
        ('word', 'epub'), ('epub', 'word'),
        ('html', 'txt'), ('txt', 'html'),
        ('rtf', 'txt'), ('txt', 'rtf'),
        ('odt', 'txt'), ('txt', 'odt'),
        ('html', 'epub'), ('epub', 'html'),
        ('word', 'ppt'), ('ppt', 'word'),
        ('html', 'odt'), ('odt', 'html'),
        ('rtf', 'odt'), ('odt', 'rtf'),
        ('rtf', 'html'), ('html', 'rtf'),
        ('csv', 'txt'), ('txt', 'csv'),
        ('epub', 'txt'), ('txt', 'epub'),
        ('epub', 'odt'), ('odt', 'epub'),
        ('rtf', 'epub'), ('epub', 'rtf'),
        ('csv', 'html'), ('html', 'csv'),
        ('ppt', 'txt'), ('txt', 'ppt'),
    ]
    for pair in cross_doc_pairs:
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)

    # Additional image-to-document pairs
    for img_key in ['webp', 'gif', 'bmp', 'tiff']:
        pair_to = (img_key, 'pdf')
        if pair_to not in seen:
            pairs.append(pair_to)
            seen.add(pair_to)

    return pairs


def get_all_pairs():
    """Get all conversion pairs."""
    return get_all_image_pairs() + get_all_document_pairs()


# Priority pairs for the index page (most searched conversions)
POPULAR_IMAGE_PAIRS = [
    ('jpg', 'png'), ('png', 'jpg'),
    ('heic', 'jpg'), ('heic', 'png'),
    ('webp', 'jpg'), ('webp', 'png'),
    ('jpg', 'webp'), ('png', 'webp'),
    ('svg', 'png'), ('svg', 'jpg'),
    ('gif', 'jpg'), ('gif', 'png'),
    ('bmp', 'jpg'), ('bmp', 'png'),
    ('tiff', 'jpg'), ('tiff', 'png'),
    ('png', 'ico'), ('jpg', 'ico'),
    ('avif', 'jpg'), ('avif', 'png'),
    ('jpg', 'avif'), ('png', 'avif'),
    ('jpg', 'gif'), ('png', 'gif'),
    ('jpg', 'bmp'), ('png', 'bmp'),
    ('jpg', 'tiff'), ('png', 'tiff'),
    ('webp', 'gif'), ('gif', 'webp'),
    ('ico', 'png'), ('ico', 'jpg'),
]

POPULAR_DOCUMENT_PAIRS = [
    ('word', 'pdf'), ('pdf', 'word'),
    ('excel', 'pdf'), ('pdf', 'excel'),
    ('ppt', 'pdf'), ('pdf', 'ppt'),
    ('jpg', 'pdf'), ('png', 'pdf'),
    ('pdf', 'jpg'), ('pdf', 'png'),
    ('csv', 'pdf'), ('pdf', 'csv'),
    ('txt', 'pdf'), ('pdf', 'txt'),
    ('html', 'pdf'), ('pdf', 'html'),
    ('odt', 'pdf'), ('pdf', 'odt'),
    ('rtf', 'pdf'), ('pdf', 'rtf'),
    ('epub', 'pdf'), ('pdf', 'epub'),
    ('word', 'txt'), ('word', 'html'),
    ('excel', 'csv'), ('csv', 'excel'),
    ('word', 'rtf'), ('rtf', 'word'),
    ('word', 'odt'), ('odt', 'word'),
    ('word', 'epub'), ('epub', 'word'),
    ('html', 'txt'), ('txt', 'html'),
    ('epub', 'txt'), ('txt', 'epub'),
    ('ppt', 'word'), ('word', 'ppt'),
]

# =============================================================================
# Auto-generated SEO content
# =============================================================================

def get_format_specific_features(source_key, target_key, conv_type):
    """Generate 3 relevant features for the conversion pair."""
    src = ALL_FORMATS[source_key]
    tgt = ALL_FORMATS[target_key]
    src_name = src['name']
    tgt_name = tgt['name']

    if conv_type == 'image-to-image':
        features = [
            {
                'title': 'Lossless Quality Conversion',
                'text': f'Convert your {src_name} files to {tgt_name} format while preserving maximum image quality. Our converter uses advanced algorithms to ensure your images look their best.',
                'icon': 'quality',
            },
            {
                'title': 'Lightning-Fast Processing',
                'text': f'Upload your {src_name} file and get your {tgt_name} download in seconds. Our server-side conversion engine processes images instantly, no matter the file size.',
                'icon': 'speed',
            },
            {
                'title': 'Secure & Private',
                'text': f'Your {src_name} files are processed securely and never stored on our servers. All conversions happen in real-time, and files are deleted immediately after download.',
                'icon': 'security',
            },
        ]
    elif 'pdf' in (source_key, target_key):
        features = [
            {
                'title': 'Accurate Conversion',
                'text': f'Convert {src_name} to {tgt_name} with accurate formatting preservation. Tables, images, fonts, and layout are maintained throughout the conversion process.',
                'icon': 'quality',
            },
            {
                'title': 'No Software Required',
                'text': f'Convert {src_name} to {tgt_name} directly in your browser. No need to install Microsoft Office, Adobe Acrobat, or any other desktop software.',
                'icon': 'speed',
            },
            {
                'title': 'Secure File Handling',
                'text': f'Your {src_name} files are encrypted during upload and processed securely. Files are automatically deleted after conversion. Your documents stay private.',
                'icon': 'security',
            },
        ]
    else:
        features = [
            {
                'title': 'High-Quality Output',
                'text': f'Get professional-quality {tgt_name} files from your {src_name} documents. Our converter preserves formatting, layout, and content integrity.',
                'icon': 'quality',
            },
            {
                'title': 'Fast & Free',
                'text': f'Convert {src_name} to {tgt_name} in seconds with no registration or payment required. Works on any device with a web browser.',
                'icon': 'speed',
            },
            {
                'title': 'Private & Secure',
                'text': f'All file processing happens securely. Your {src_name} documents are never stored and are deleted immediately after conversion.',
                'icon': 'security',
            },
        ]

    return features


def get_format_specific_faqs(source_key, target_key, conv_type):
    """Generate 4 relevant FAQs for the conversion pair."""
    src = ALL_FORMATS[source_key]
    tgt = ALL_FORMATS[target_key]
    src_name = src['name']
    tgt_name = tgt['name']
    src_lower = source_key
    tgt_lower = target_key

    faqs = [
        {
            'q': f'How do I convert {src_name} to {tgt_name}?',
            'a': f'Simply upload your {src_name} file using the upload area above, then click the "Convert to {tgt_name}" button. Your converted {tgt_name} file will be ready to download in seconds.',
        },
        {
            'q': f'Is this {src_name} to {tgt_name} converter free?',
            'a': f'Yes, our {src_name} to {tgt_name} converter is completely free to use. There is no registration required, no watermarks are added, and there are no hidden fees.',
        },
        {
            'q': f'Will I lose quality when converting from {src_name} to {tgt_name}?',
            'a': _get_quality_answer(source_key, target_key, src_name, tgt_name),
        },
        {
            'q': f'Can I convert {tgt_name} back to {src_name}?',
            'a': (
                f'Yes! We also offer a <a href="/convert/{tgt_lower}-to-{src_lower}/">'
                f'{tgt_name} to {src_name} converter</a>. You can convert between these '
                f'formats in both directions.'
            ),
        },
    ]

    return faqs


def _get_quality_answer(source_key, target_key, src_name, tgt_name):
    """Generate a quality-specific FAQ answer based on the format characteristics."""
    lossy = {'jpg', 'webp', 'avif', 'gif'}
    lossless = {'png', 'bmp', 'tiff', 'ico', 'svg'}

    if source_key in lossless and target_key in lossless:
        return (
            f'No. Both {src_name} and {tgt_name} are lossless formats, so the conversion '
            f'preserves the exact pixel data of your original image without any quality loss.'
        )
    elif source_key in lossy and target_key in lossless:
        return (
            f'The conversion preserves the quality of your {src_name} file exactly as-is. '
            f'Since {tgt_name} is a lossless format, no additional quality loss occurs during conversion.'
        )
    elif target_key in lossy:
        return (
            f'{tgt_name} uses lossy compression, so there may be a very slight reduction in quality. '
            f'However, our converter uses optimal settings to minimize any visible quality loss. '
            f'You can also adjust the quality slider to balance file size and image quality.'
        )
    else:
        return (
            f'Our converter is designed to preserve maximum quality during the {src_name} to {tgt_name} '
            f'conversion. The output closely matches the original in terms of content and formatting.'
        )


def get_how_to_steps(source_key, target_key):
    """Generate how-to steps for the conversion."""
    src_name = ALL_FORMATS[source_key]['name']
    tgt_name = ALL_FORMATS[target_key]['name']

    return [
        {
            'step': 1,
            'title': f'Upload Your {src_name} File',
            'text': f'Click the upload area or drag and drop your {src_name} file. You can upload any {src_name} file from your computer, phone, or tablet.',
        },
        {
            'step': 2,
            'title': f'Convert to {tgt_name}',
            'text': f'Click the "Convert to {tgt_name}" button to start the conversion. The process typically takes just a few seconds.',
        },
        {
            'step': 3,
            'title': f'Download Your {tgt_name} File',
            'text': f'Once the conversion is complete, click the download button to save your new {tgt_name} file to your device.',
        },
    ]


# =============================================================================
# Views
# =============================================================================

class ConverterIndexPage(View):
    """
    Index page at /convert/ listing all available file conversions
    organized by category.
    """

    def get(self, request):
        g = GlobalVars.get_globals(request)

        # Build categorized pairs
        image_pairs = []
        for src, tgt in get_all_image_pairs():
            image_pairs.append({
                'source': IMAGE_FORMATS[src],
                'target': IMAGE_FORMATS[tgt],
                'url': f'/convert/{src}-to-{tgt}/',
                'label': f'{IMAGE_FORMATS[src]["name"]} to {IMAGE_FORMATS[tgt]["name"]}',
            })

        doc_pairs = []
        for src, tgt in get_all_document_pairs():
            src_fmt = ALL_FORMATS[src]
            tgt_fmt = ALL_FORMATS[tgt]
            doc_pairs.append({
                'source': src_fmt,
                'target': tgt_fmt,
                'url': f'/convert/{src}-to-{tgt}/',
                'label': f'{src_fmt["name"]} to {tgt_fmt["name"]}',
            })

        # Popular pairs for hero section
        popular = []
        for src, tgt in (POPULAR_IMAGE_PAIRS[:12] + POPULAR_DOCUMENT_PAIRS[:8]):
            src_fmt = ALL_FORMATS[src]
            tgt_fmt = ALL_FORMATS[tgt]
            popular.append({
                'source': src_fmt,
                'target': tgt_fmt,
                'url': f'/convert/{src}-to-{tgt}/',
                'label': f'{src_fmt["name"]} to {tgt_fmt["name"]}',
            })

        total_count = len(image_pairs) + len(doc_pairs)

        return render(request, 'converter/index.html', {
            'title': f'Free Online File Converter - {total_count}+ Formats | {config.PROJECT_NAME}',
            'description': f'Convert files between {total_count}+ format combinations. Image converter, document converter, PDF tools and more. Free online, no registration.',
            'page': 'converter',
            'g': g,
            'image_pairs': image_pairs,
            'doc_pairs': doc_pairs,
            'popular': popular,
            'total_count': total_count,
            'image_formats': IMAGE_FORMATS,
            'document_formats': DOCUMENT_FORMATS,
        })


class ConverterPairPage(View):
    """
    SEO landing page for a specific conversion pair.
    e.g. /convert/jpg-to-png/, /convert/word-to-pdf/
    """

    def get(self, request, source, target):
        source_key = source.lower()
        target_key = target.lower()

        # Validate both formats exist
        if source_key not in ALL_FORMATS or target_key not in ALL_FORMATS:
            raise Http404

        # Cannot convert to same format
        if source_key == target_key:
            raise Http404

        src = ALL_FORMATS[source_key]
        tgt = ALL_FORMATS[target_key]
        conv_type = get_conversion_type(source_key, target_key)

        # Determine API configuration
        api_config = get_api_config(source_key, target_key, conv_type)
        accept = get_accept_string(source_key, conv_type, api_config)

        # Generate SEO content
        seo = {
            'h1': f'Convert {src["name"]} to {tgt["name"]} Online Free',
            'subtitle': (
                f'Free online {src["name"]} to {tgt["name"]} converter. '
                f'Upload your {src["name"]} file and download it as {tgt["name"]} instantly. '
                f'No registration required.'
            ),
            'meta_title': f'{src["name"]} to {tgt["name"]} Converter - Free Online | {config.PROJECT_NAME}',
            'meta_description': (
                f'Convert {src["name"]} to {tgt["name"]} online for free. '
                f'No registration required. Fast, secure file conversion powered by {config.PROJECT_NAME}.'
            ),
            'features': get_format_specific_features(source_key, target_key, conv_type),
            'faqs': get_format_specific_faqs(source_key, target_key, conv_type),
            'steps': get_how_to_steps(source_key, target_key),
        }

        # Build "other popular conversions" links
        other_pairs = _get_related_pairs(source_key, target_key, conv_type)

        g = GlobalVars.get_globals(request)

        return render(request, 'converter/pair.html', {
            'title': seo['meta_title'],
            'description': seo['meta_description'],
            'page': 'converter',
            'g': g,
            'seo': seo,
            'source_key': source_key,
            'target_key': target_key,
            'source_fmt': src,
            'target_fmt': tgt,
            'conv_type': conv_type,
            'api_config': api_config,
            'accept': accept,
            'other_pairs': other_pairs,
        })


def _get_related_pairs(source_key, target_key, conv_type):
    """Build a list of related conversion pairs for cross-linking."""
    pairs = []
    seen = set()
    seen.add((source_key, target_key))

    # 1. Reverse pair
    if target_key in ALL_FORMATS and source_key in ALL_FORMATS:
        pair = (target_key, source_key)
        if pair not in seen:
            seen.add(pair)
            pairs.append({
                'source_name': ALL_FORMATS[target_key]['name'],
                'target_name': ALL_FORMATS[source_key]['name'],
                'url': f'/convert/{target_key}-to-{source_key}/',
            })

    # 2. Same source, different targets
    if conv_type == 'image-to-image':
        priority_list = POPULAR_IMAGE_PAIRS
    else:
        priority_list = POPULAR_DOCUMENT_PAIRS

    for s, t in priority_list:
        if (s, t) not in seen:
            seen.add((s, t))
            pairs.append({
                'source_name': ALL_FORMATS[s]['name'],
                'target_name': ALL_FORMATS[t]['name'],
                'url': f'/convert/{s}-to-{t}/',
            })
        if len(pairs) >= 20:
            break

    # Pad with more pairs from the other category if needed
    if len(pairs) < 20:
        other_list = POPULAR_DOCUMENT_PAIRS if conv_type == 'image-to-image' else POPULAR_IMAGE_PAIRS
        for s, t in other_list:
            if (s, t) not in seen:
                seen.add((s, t))
                pairs.append({
                    'source_name': ALL_FORMATS[s]['name'],
                    'target_name': ALL_FORMATS[t]['name'],
                    'url': f'/convert/{s}-to-{t}/',
                })
            if len(pairs) >= 20:
                break

    return pairs
