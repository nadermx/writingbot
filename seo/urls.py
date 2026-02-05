from django.urls import path

from seo.views import (
    RewordingToolPage, SentenceRewriterPage, ParagraphRewriterPage,
    EssayRewriterPage, ArticleRewriterPage, TextRewriterPage,
    SpellCheckerPage, PunctuationCheckerPage, EssayCheckerPage,
    OnlineProofreaderPage,
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
]
