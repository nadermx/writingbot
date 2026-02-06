from django.urls import path

from seo.views import (
    RewordingToolPage, SentenceRewriterPage, ParagraphRewriterPage,
    EssayRewriterPage, ArticleRewriterPage, TextRewriterPage,
    SpellCheckerPage, PunctuationCheckerPage, EssayCheckerPage,
    OnlineProofreaderPage,
    GermanGrammarCheckPage, FrenchGrammarCheckPage, SpanishGrammarCheckPage,
    PortugueseGrammarCheckPage, DutchGrammarCheckPage, ItalianGrammarCheckPage,
    PolishGrammarCheckPage, SwedishGrammarCheckPage, RussianGrammarCheckPage,
    JapaneseGrammarCheckPage,
    GuidesIndexPage, GuidePage,
)

urlpatterns = [
    path('rewording-tool/', RewordingToolPage.as_view(), name='rewording_tool'),
    path('sentence-rewriter/', SentenceRewriterPage.as_view(), name='sentence_rewriter'),
    path('paragraph-rewriter/', ParagraphRewriterPage.as_view(), name='paragraph_rewriter'),
    path('essay-rewriter/', EssayRewriterPage.as_view(), name='essay_rewriter'),
    path('article-rewriter/', ArticleRewriterPage.as_view(), name='article_rewriter'),
    path('text-rewriter/', TextRewriterPage.as_view(), name='text_rewriter'),
    path('spell-checker/', SpellCheckerPage.as_view(), name='spell_checker'),
    path('punctuation-checker/', PunctuationCheckerPage.as_view(), name='punctuation_checker'),
    path('essay-checker/', EssayCheckerPage.as_view(), name='essay_checker'),
    path('online-proofreader/', OnlineProofreaderPage.as_view(), name='online_proofreader'),
    # Language-specific grammar checker SEO pages
    path('german-grammar-check/', GermanGrammarCheckPage.as_view(), name='german_grammar_check'),
    path('french-grammar-check/', FrenchGrammarCheckPage.as_view(), name='french_grammar_check'),
    path('spanish-grammar-check/', SpanishGrammarCheckPage.as_view(), name='spanish_grammar_check'),
    path('portuguese-grammar-check/', PortugueseGrammarCheckPage.as_view(), name='portuguese_grammar_check'),
    path('dutch-grammar-check/', DutchGrammarCheckPage.as_view(), name='dutch_grammar_check'),
    path('italian-grammar-check/', ItalianGrammarCheckPage.as_view(), name='italian_grammar_check'),
    path('polish-grammar-check/', PolishGrammarCheckPage.as_view(), name='polish_grammar_check'),
    path('swedish-grammar-check/', SwedishGrammarCheckPage.as_view(), name='swedish_grammar_check'),
    path('russian-grammar-check/', RussianGrammarCheckPage.as_view(), name='russian_grammar_check'),
    path('japanese-grammar-check/', JapaneseGrammarCheckPage.as_view(), name='japanese_grammar_check'),
    # Guides
    path('guides/', GuidesIndexPage.as_view(), name='guides_index'),
    path('guides/paraphrasing/', GuidePage.as_view(guide_key='paraphrasing'), name='guide_paraphrasing'),
    path('guides/grammar/', GuidePage.as_view(guide_key='grammar'), name='guide_grammar'),
    path('guides/ai-writing-assistant/', GuidePage.as_view(guide_key='ai-writing-assistant'), name='guide_ai_writing_assistant'),
    path('guides/apa-citation/', GuidePage.as_view(guide_key='apa-citation'), name='guide_apa_citation'),
    path('guides/mla-citation/', GuidePage.as_view(guide_key='mla-citation'), name='guide_mla_citation'),
    path('guides/chicago-citation/', GuidePage.as_view(guide_key='chicago-citation'), name='guide_chicago_citation'),
    path('guides/academic-writing/', GuidePage.as_view(guide_key='academic-writing'), name='guide_academic_writing'),
    path('guides/business-writing/', GuidePage.as_view(guide_key='business-writing'), name='guide_business_writing'),
    path('guides/essay-writing/', GuidePage.as_view(guide_key='essay-writing'), name='guide_essay_writing'),
    path('guides/plagiarism-prevention/', GuidePage.as_view(guide_key='plagiarism-prevention'), name='guide_plagiarism_prevention'),
]
