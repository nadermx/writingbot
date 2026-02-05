from django.urls import path
from summarizer.views import SummarizerPage, SummarizeAPI

urlpatterns = [
    path('summarize/', SummarizerPage.as_view(), name='summarizer'),
    path('api/summarize/', SummarizeAPI.as_view(), name='summarize_api'),
]
