"""Tests for PDF tools service (no LLM mock needed for most operations)."""
import io
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

try:
    from pypdf import PdfWriter
    HAS_PYPDF = True
except ImportError:
    try:
        from PyPDF2 import PdfWriter
        HAS_PYPDF = True
    except ImportError:
        HAS_PYPDF = False


def make_test_pdf(num_pages=3):
    """Create a minimal valid PDF file for testing."""
    if not HAS_PYPDF:
        return None
    try:
        from pypdf import PdfWriter as Writer
    except ImportError:
        from PyPDF2 import PdfWriter as Writer
    writer = Writer()
    for _ in range(num_pages):
        writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return SimpleUploadedFile('test.pdf', buf.read(), content_type='application/pdf')


@unittest.skipUnless(HAS_PYPDF, 'pypdf/PyPDF2 not installed')
class PDFServiceTests(TestCase):

    def test_merge_pdfs(self):
        from pdf_tools.services import PDFService
        pdf1 = make_test_pdf(2)
        pdf2 = make_test_pdf(3)
        result, error = PDFService.merge_pdfs([pdf1, pdf2])
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_split_pdf_all(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(3)
        result, error = PDFService.split_pdf(pdf, 'all')
        self.assertIsNone(error)

    def test_split_pdf_specific_pages(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(5)
        result, error = PDFService.split_pdf(pdf, '1,3,5')
        self.assertIsNone(error)

    def test_compress_pdf(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(2)
        result, error = PDFService.compress_pdf(pdf, quality='medium')
        self.assertIsNone(error)

    def test_rotate_page(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(2)
        result, error = PDFService.rotate_page(pdf, page_number=1, angle=90)
        self.assertIsNone(error)

    def test_get_pdf_info(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(3)
        info, error = PDFService.get_pdf_info(pdf)
        self.assertIsNone(error)
        self.assertEqual(info['page_count'], 3)

    def test_extract_text(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(1)
        text, error = PDFService.extract_text(pdf)
        self.assertIsNone(error)
        self.assertIsNotNone(text)

    def test_remove_pages(self):
        from pdf_tools.services import PDFService
        pdf = make_test_pdf(5)
        result, error = PDFService.remove_pages(pdf, '2,4')
        self.assertIsNone(error)
