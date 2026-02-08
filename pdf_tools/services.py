import io
import json
import logging
import os
import tempfile

from django.conf import settings
from core.llm_client import LLMClient

logger = logging.getLogger('app')


class PDFService:
    """
    Service layer for PDF file operations.
    Uses PyPDF for PDF manipulation and LibreOffice for format conversions.
    """

    @staticmethod
    def merge_pdfs(files):
        """
        Merge multiple PDF files into one.

        Args:
            files: List of UploadedFile objects (PDF).

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            writer = PdfWriter()
            for f in files:
                reader = PdfReader(f)
                for page in reader.pages:
                    writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF merge failed: {e}')
            return None, 'Failed to merge PDFs. Please ensure all files are valid PDFs.'

    @staticmethod
    def split_pdf(file, pages):
        """
        Split a PDF into individual pages or page ranges.

        Args:
            file: UploadedFile object (PDF).
            pages: String specifying pages, e.g. "1,3,5-7" or "all".

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            reader = PdfReader(file)
            total_pages = len(reader.pages)
            page_indices = PDFService._parse_page_ranges(pages, total_pages)

            if not page_indices:
                return None, 'No valid pages specified.'

            writer = PdfWriter()
            for idx in page_indices:
                writer.add_page(reader.pages[idx])

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF split failed: {e}')
            return None, 'Failed to split PDF. Please check your page selections.'

    @staticmethod
    def compress_pdf(file, quality='medium'):
        """
        Compress a PDF to reduce file size.

        Args:
            file: UploadedFile object (PDF).
            quality: 'low', 'medium', or 'high' compression.

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            reader = PdfReader(file)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            for page in writer.pages:
                page.compress_content_streams()

            # Remove metadata to save space
            writer.add_metadata({})

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF compress failed: {e}')
            return None, 'Failed to compress PDF.'

    @staticmethod
    def rotate_page(file, page_number, angle):
        """
        Rotate a specific page in a PDF.

        Args:
            file: UploadedFile object (PDF).
            page_number: 1-based page number to rotate.
            angle: Rotation angle (90, 180, 270).

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            if angle not in (90, 180, 270):
                return None, 'Rotation angle must be 90, 180, or 270 degrees.'

            reader = PdfReader(file)
            writer = PdfWriter()

            for i, page in enumerate(reader.pages):
                if i == page_number - 1:
                    page.rotate(angle)
                writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF rotate failed: {e}')
            return None, 'Failed to rotate PDF page.'

    @staticmethod
    def remove_pages(file, pages):
        """
        Remove specified pages from a PDF.

        Args:
            file: UploadedFile object (PDF).
            pages: String specifying pages to remove, e.g. "1,3,5-7".

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            reader = PdfReader(file)
            total_pages = len(reader.pages)
            remove_indices = set(PDFService._parse_page_ranges(pages, total_pages))

            if not remove_indices:
                return None, 'No valid pages specified for removal.'

            if len(remove_indices) >= total_pages:
                return None, 'Cannot remove all pages from the PDF.'

            writer = PdfWriter()
            for i, page in enumerate(reader.pages):
                if i not in remove_indices:
                    writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF remove pages failed: {e}')
            return None, 'Failed to remove pages from PDF.'

    @staticmethod
    def reorder_pages(file, order):
        """
        Reorder pages in a PDF.

        Args:
            file: UploadedFile object (PDF).
            order: List of 1-based page numbers in desired order, e.g. [3, 1, 2].

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            from pypdf import PdfReader, PdfWriter

            reader = PdfReader(file)
            total_pages = len(reader.pages)

            # Validate order
            if not order or not isinstance(order, list):
                return None, 'Please provide a valid page order.'

            indices = []
            for p in order:
                idx = int(p) - 1
                if idx < 0 or idx >= total_pages:
                    return None, f'Page {p} is out of range (1-{total_pages}).'
                indices.append(idx)

            writer = PdfWriter()
            for idx in indices:
                writer.add_page(reader.pages[idx])

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'PDF reorder failed: {e}')
            return None, 'Failed to reorder PDF pages.'

    @staticmethod
    def convert_to_pdf(file, source_format):
        """
        Convert a file (DOCX, PPTX, JPG, PNG) to PDF using LibreOffice or Pillow.

        Args:
            file: UploadedFile object.
            source_format: File extension string (e.g. 'docx', 'jpg', 'png', 'pptx').

        Returns:
            Tuple of (BytesIO output, error).
        """
        try:
            source_format = source_format.lower().strip('.')

            if source_format in ('jpg', 'jpeg', 'png'):
                return PDFService._image_to_pdf(file)
            elif source_format in ('docx', 'doc', 'pptx', 'ppt'):
                return PDFService._office_to_pdf(file, source_format)
            else:
                return None, f'Unsupported format: {source_format}'

        except Exception as e:
            logger.error(f'Convert to PDF failed: {e}')
            return None, 'Failed to convert file to PDF.'

    @staticmethod
    def convert_from_pdf(file, target_format):
        """
        Convert a PDF to another format (DOCX, JPG, PNG, PPTX).

        Args:
            file: UploadedFile object (PDF).
            target_format: Target extension string (e.g. 'docx', 'jpg', 'png', 'pptx').

        Returns:
            Tuple of (BytesIO output or list of BytesIO for images, error).
        """
        try:
            target_format = target_format.lower().strip('.')

            if target_format in ('jpg', 'jpeg', 'png'):
                return PDFService._pdf_to_images(file, target_format)
            elif target_format in ('docx', 'pptx'):
                return PDFService._pdf_to_office(file, target_format)
            else:
                return None, f'Unsupported target format: {target_format}'

        except Exception as e:
            logger.error(f'Convert from PDF failed: {e}')
            return None, 'Failed to convert PDF.'

    @staticmethod
    def extract_text(file):
        """
        Extract all text from a PDF file.

        Args:
            file: UploadedFile object (PDF).

        Returns:
            Tuple of (text_string, error).
        """
        try:
            from pypdf import PdfReader

            reader = PdfReader(file)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            full_text = '\n\n'.join(text_parts)
            return full_text, None

        except Exception as e:
            logger.error(f'PDF text extraction failed: {e}')
            return None, 'Failed to extract text from PDF.'

    @staticmethod
    def chat_with_pdf(file, question, use_premium=False):
        """
        Answer a question about a PDF's contents using Claude API.

        Args:
            file: UploadedFile object (PDF).
            question: User question string.
            use_premium: If True, use premium Claude API.

        Returns:
            Tuple of (answer_string, error).
        """
        try:
            text, err = PDFService.extract_text(file)
            if err:
                return None, err

            if not text or not text.strip():
                return None, 'Could not extract any text from this PDF.'

            # Truncate to reasonable size for the API
            max_chars = 50000
            if len(text) > max_chars:
                text = text[:max_chars] + '\n\n[Document truncated due to length...]'

            answer, error = LLMClient.generate(
                system_prompt=(
                    'You are a helpful document analysis assistant. The user has uploaded a PDF document '
                    'and wants to ask questions about it. Answer based ONLY on the document content provided. '
                    'If the answer is not in the document, say so. Be concise and accurate.'
                ),
                messages=[
                    {
                        'role': 'user',
                        'content': f'Document content:\n\n{text}\n\n---\n\nQuestion: {question}'
                    }
                ],
                max_tokens=2048,
                use_premium=use_premium
            )

            if error:
                return None, error

            return answer, None

        except Exception as e:
            logger.error(f'ChatPDF failed: {e}')
            return None, 'Failed to process your question about the PDF.'

    @staticmethod
    def get_pdf_info(file):
        """
        Get metadata and page count from a PDF.

        Args:
            file: UploadedFile object (PDF).

        Returns:
            Tuple of (info_dict, error).
        """
        try:
            from pypdf import PdfReader

            reader = PdfReader(file)
            meta = reader.metadata or {}

            info = {
                'page_count': len(reader.pages),
                'title': meta.get('/Title', ''),
                'author': meta.get('/Author', ''),
                'subject': meta.get('/Subject', ''),
                'creator': meta.get('/Creator', ''),
            }

            # Get first page dimensions
            if reader.pages:
                first_page = reader.pages[0]
                box = first_page.mediabox
                info['width'] = float(box.width)
                info['height'] = float(box.height)

            return info, None

        except Exception as e:
            logger.error(f'PDF info extraction failed: {e}')
            return None, 'Failed to read PDF information.'

    # --- Private helpers ---

    @staticmethod
    def _parse_page_ranges(pages_str, total_pages):
        """
        Parse a page range string like "1,3,5-7" into a list of 0-based indices.
        """
        if not pages_str or pages_str.strip().lower() == 'all':
            return list(range(total_pages))

        indices = []
        parts = pages_str.replace(' ', '').split(',')

        for part in parts:
            if '-' in part:
                try:
                    start, end = part.split('-', 1)
                    start = int(start) - 1
                    end = int(end) - 1
                    for i in range(max(0, start), min(total_pages, end + 1)):
                        if i not in indices:
                            indices.append(i)
                except ValueError:
                    continue
            else:
                try:
                    idx = int(part) - 1
                    if 0 <= idx < total_pages and idx not in indices:
                        indices.append(idx)
                except ValueError:
                    continue

        return indices

    @staticmethod
    def _image_to_pdf(file):
        """Convert an image file (JPG/PNG) to PDF using Pillow."""
        try:
            from PIL import Image

            img = Image.open(file)
            if img.mode == 'RGBA':
                # Convert RGBA to RGB for PDF compatibility
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            output = io.BytesIO()
            img.save(output, 'PDF', resolution=150.0)
            output.seek(0)
            return output, None

        except Exception as e:
            logger.error(f'Image to PDF conversion failed: {e}')
            return None, 'Failed to convert image to PDF.'

    @staticmethod
    def _office_to_pdf(file, source_format):
        """Convert an Office document to PDF using LibreOffice."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, f'input.{source_format}')
                with open(input_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                import subprocess
                result = subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', tmpdir, input_path],
                    capture_output=True, timeout=60
                )

                if result.returncode != 0:
                    logger.error(f'LibreOffice conversion failed: {result.stderr.decode()}')
                    return None, 'Document conversion failed.'

                output_path = os.path.join(tmpdir, 'input.pdf')
                if not os.path.exists(output_path):
                    return None, 'Conversion produced no output.'

                output = io.BytesIO()
                with open(output_path, 'rb') as f:
                    output.write(f.read())
                output.seek(0)
                return output, None

        except subprocess.TimeoutExpired:
            return None, 'Conversion timed out. The file may be too large.'
        except Exception as e:
            logger.error(f'Office to PDF conversion failed: {e}')
            return None, 'Failed to convert document to PDF.'

    @staticmethod
    def _pdf_to_images(file, target_format):
        """Convert PDF pages to images using pdf2image."""
        try:
            import subprocess
            from PIL import Image

            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, 'input.pdf')
                with open(input_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                try:
                    from pdf2image import convert_from_path
                    images = convert_from_path(input_path, dpi=200, output_folder=tmpdir)
                except ImportError:
                    return None, 'PDF to image conversion is not available. Please install pdf2image.'

                if not images:
                    return None, 'No pages found in PDF.'

                if len(images) == 1:
                    output = io.BytesIO()
                    fmt = 'JPEG' if target_format in ('jpg', 'jpeg') else 'PNG'
                    images[0].save(output, fmt, quality=90)
                    output.seek(0)
                    return output, None
                else:
                    # Multiple pages: return as zip
                    import zipfile
                    zip_buffer = io.BytesIO()
                    fmt = 'JPEG' if target_format in ('jpg', 'jpeg') else 'PNG'
                    ext = 'jpg' if target_format in ('jpg', 'jpeg') else 'png'
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                        for i, img in enumerate(images):
                            img_buffer = io.BytesIO()
                            img.save(img_buffer, fmt, quality=90)
                            img_buffer.seek(0)
                            zf.writestr(f'page_{i + 1}.{ext}', img_buffer.read())
                    zip_buffer.seek(0)
                    return zip_buffer, None

        except Exception as e:
            logger.error(f'PDF to images conversion failed: {e}')
            return None, 'Failed to convert PDF to images.'

    @staticmethod
    def _pdf_to_office(file, target_format):
        """Convert PDF to Office document using LibreOffice."""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                input_path = os.path.join(tmpdir, 'input.pdf')
                with open(input_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                import subprocess
                result = subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', target_format, '--outdir', tmpdir, input_path],
                    capture_output=True, timeout=60
                )

                if result.returncode != 0:
                    logger.error(f'LibreOffice PDF conversion failed: {result.stderr.decode()}')
                    return None, 'Document conversion failed.'

                output_path = os.path.join(tmpdir, f'input.{target_format}')
                if not os.path.exists(output_path):
                    return None, 'Conversion produced no output.'

                output = io.BytesIO()
                with open(output_path, 'rb') as f:
                    output.write(f.read())
                output.seek(0)
                return output, None

        except subprocess.TimeoutExpired:
            return None, 'Conversion timed out. The file may be too large.'
        except Exception as e:
            logger.error(f'PDF to Office conversion failed: {e}')
            return None, f'Failed to convert PDF to {target_format.upper()}.'
