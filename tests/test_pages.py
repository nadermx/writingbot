"""
Test that all public page URLs return HTTP 200.
Catches template rendering errors, missing context, broken imports, etc.
"""
from django.test import TestCase, Client


class PublicPageTests(TestCase):
    """Test all public-facing pages return 200."""

    def setUp(self):
        self.client = Client()

    def _get(self, url, expected_status=200):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, expected_status,
            f'{url} returned {response.status_code}, expected {expected_status}'
        )
        return response

    # ------------------------------------------------------------------
    # Core pages
    # ------------------------------------------------------------------
    def test_index(self):
        self._get('/')

    def test_login(self):
        self._get('/login/')

    def test_signup(self):
        self._get('/signup/')

    def test_lost_password(self):
        self._get('/lost-password/')

    def test_pricing(self):
        self._get('/pricing/')

    def test_contact(self):
        self._get('/contact/')

    def test_about(self):
        self._get('/about/')

    def test_terms(self):
        self._get('/terms/')

    def test_privacy(self):
        self._get('/privacy/')

    def test_refund(self):
        self._get('/refund/')

    def test_help(self):
        self._get('/help/')

    def test_trust_center(self):
        self._get('/trust-center/')

    def test_student_resources(self):
        self._get('/student-resources/')

    def test_professionals(self):
        self._get('/professionals/')

    # ------------------------------------------------------------------
    # Tool pages
    # ------------------------------------------------------------------
    def test_paraphraser(self):
        self._get('/paraphrasing-tool/')

    def test_grammar(self):
        self._get('/grammar-check/')

    def test_summarizer(self):
        self._get('/summarize/')

    def test_ai_detector(self):
        self._get('/ai-content-detector/')

    def test_humanizer(self):
        self._get('/ai-humanizer/')

    def test_plagiarism(self):
        self._get('/plagiarism-checker/')

    def test_translator(self):
        self._get('/translate/')

    def test_citations(self):
        self._get('/citation-generator/')

    def test_word_counter(self):
        self._get('/word-counter/')

    # ------------------------------------------------------------------
    # Flow
    # ------------------------------------------------------------------
    def test_flow(self):
        self._get('/flow/')

    def test_ai_chat(self):
        self._get('/ai-chat/')

    def test_ai_search(self):
        self._get('/ai-search/')

    # ------------------------------------------------------------------
    # AI Tools
    # ------------------------------------------------------------------
    def test_ai_tools_index(self):
        self._get('/ai-writing-tools/')

    # ------------------------------------------------------------------
    # PDF Tools
    # ------------------------------------------------------------------
    def test_pdf_tools_index(self):
        self._get('/pdf-tools/')

    # ------------------------------------------------------------------
    # Media Tools
    # ------------------------------------------------------------------
    def test_image_tools(self):
        self._get('/image-tools/')

    def test_converter_tools(self):
        self._get('/converter-tools/')

    def test_background_remover(self):
        self._get('/background-remover/')

    def test_qr_code_generator(self):
        self._get('/tools/qr-code-generator/')

    def test_voice_generator(self):
        self._get('/tools/ai-voice-generator/')

    def test_transcription(self):
        self._get('/tools/transcription/')

    def test_logo_generator(self):
        self._get('/tools/logo-generator/')

    def test_character_generator(self):
        self._get('/tools/character-generator/')

    def test_word_cloud(self):
        self._get('/tools/word-cloud/')

    def test_banner_generator(self):
        self._get('/tools/banner-generator/')

    def test_presentation_maker(self):
        self._get('/tools/presentation-maker/')

    def test_media_tools_index(self):
        self._get('/media-tools/')

    # ------------------------------------------------------------------
    # SEO landing pages
    # ------------------------------------------------------------------
    def test_rewording_tool(self):
        self._get('/rewording-tool/')

    def test_sentence_rewriter(self):
        self._get('/sentence-rewriter/')

    def test_paragraph_rewriter(self):
        self._get('/paragraph-rewriter/')

    def test_essay_rewriter(self):
        self._get('/essay-rewriter/')

    def test_article_rewriter(self):
        self._get('/article-rewriter/')

    def test_text_rewriter(self):
        self._get('/text-rewriter/')

    def test_spell_checker(self):
        self._get('/spell-checker/')

    def test_punctuation_checker(self):
        self._get('/punctuation-checker/')

    def test_essay_checker(self):
        self._get('/essay-checker/')

    def test_online_proofreader(self):
        self._get('/online-proofreader/')

    # ------------------------------------------------------------------
    # Blog / Courses index
    # ------------------------------------------------------------------
    def test_blog_index(self):
        self._get('/blog/')

    def test_courses_index(self):
        self._get('/courses/')

    # ------------------------------------------------------------------
    # API docs
    # ------------------------------------------------------------------
    def test_api_docs(self):
        self._get('/api/docs/')
