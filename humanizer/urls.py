from django.urls import path
from humanizer.views import HumanizerPage, HumanizeAPI

urlpatterns = [
    path('ai-humanizer/', HumanizerPage.as_view(), name='humanizer'),
    path('api/humanize/', HumanizeAPI.as_view(), name='humanize_api'),
]
