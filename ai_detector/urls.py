from django.urls import path
from ai_detector.views import AIDetectorPage, AIDetectAPI

urlpatterns = [
    path('ai-content-detector/', AIDetectorPage.as_view(), name='ai_detector'),
    path('api/ai-detect/', AIDetectAPI.as_view(), name='ai_detect_api'),
]
