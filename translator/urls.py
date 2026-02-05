from django.urls import path
from translator.views import TranslatorPage, TranslateAPI, LanguagesAPI

urlpatterns = [
    path('translate/', TranslatorPage.as_view(), name='translator'),
    path('api/translate/', TranslateAPI.as_view(), name='translate_api'),
    path('api/translate/languages/', LanguagesAPI.as_view(), name='languages_api'),
]
