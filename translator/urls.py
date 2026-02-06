from django.urls import path
from translator.views import TranslatorPage, TranslateAPI, LanguagesAPI, TranslationPairPage

urlpatterns = [
    path('translate/', TranslatorPage.as_view(), name='translator'),
    path('translate/<str:source>-to-<str:target>/', TranslationPairPage.as_view(), name='translation_pair'),
    path('api/translate/', TranslateAPI.as_view(), name='translate_api'),
    path('api/translate/languages/', LanguagesAPI.as_view(), name='languages_api'),
]
