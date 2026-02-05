from django.urls import path
from plagiarism.views import PlagiarismPage, PlagiarismCheckAPI, PlagiarismUsageAPI

urlpatterns = [
    path('plagiarism-checker/', PlagiarismPage.as_view(), name='plagiarism'),
    path('api/plagiarism/check/', PlagiarismCheckAPI.as_view(), name='plagiarism_check'),
    path('api/plagiarism/usage/', PlagiarismUsageAPI.as_view(), name='plagiarism_usage'),
]
