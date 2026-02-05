from django.urls import path

from api.views import (
    APIDocsPage,
    ParaphraseAPIv1, GrammarAPIv1, SummarizeAPIv1,
    AIDetectAPIv1, TranslateAPIv1,
)

urlpatterns = [
    # Documentation page
    path('docs/', APIDocsPage.as_view(), name='api_docs'),

    # v1 API endpoints
    path('v1/paraphrase/', ParaphraseAPIv1.as_view(), name='api_v1_paraphrase'),
    path('v1/grammar/', GrammarAPIv1.as_view(), name='api_v1_grammar'),
    path('v1/summarize/', SummarizeAPIv1.as_view(), name='api_v1_summarize'),
    path('v1/ai-detect/', AIDetectAPIv1.as_view(), name='api_v1_ai_detect'),
    path('v1/translate/', TranslateAPIv1.as_view(), name='api_v1_translate'),
]
