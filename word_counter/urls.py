from django.urls import path
from word_counter.views import WordCounterPage

urlpatterns = [
    path('word-counter/', WordCounterPage.as_view(), name='word_counter'),
]
