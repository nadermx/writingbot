from django.urls import path
from grammar.views import (
    GrammarPage, GrammarCheckAPI, GrammarFixAPI,
    ProofreaderPage, ProofreadAPI, ProofreadDownloadAPI,
)

urlpatterns = [
    path('grammar-check/', GrammarPage.as_view(), name='grammar'),
    path('api/grammar/check/', GrammarCheckAPI.as_view(), name='grammar_check_api'),
    path('api/grammar/fix/', GrammarFixAPI.as_view(), name='grammar_fix_api'),
    # Proofreader
    path('proofreader/', ProofreaderPage.as_view(), name='proofreader'),
    path('api/proofread/', ProofreadAPI.as_view(), name='proofread_api'),
    path('api/proofread/download/', ProofreadDownloadAPI.as_view(), name='proofread_download_api'),
]
