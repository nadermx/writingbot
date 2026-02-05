from django.urls import path
from grammar.views import GrammarPage, GrammarCheckAPI, GrammarFixAPI

urlpatterns = [
    path('grammar-check/', GrammarPage.as_view(), name='grammar'),
    path('api/grammar/check/', GrammarCheckAPI.as_view(), name='grammar_check_api'),
    path('api/grammar/fix/', GrammarFixAPI.as_view(), name='grammar_fix_api'),
]
