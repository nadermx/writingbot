from django.urls import path
from word_counter.views import WordCounterPage, CharacterCounterPage, TextCaseConverterPage

urlpatterns = [
    path('word-counter/', WordCounterPage.as_view(), name='word_counter'),
    path('character-counter/', CharacterCounterPage.as_view(), name='character_counter'),
    path('text-case-converter/', TextCaseConverterPage.as_view(), name='text_case_converter'),
]
