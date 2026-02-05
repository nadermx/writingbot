from django.urls import path
from citations.views import CitationPage, GenerateCitationAPI, AutociteAPI, CitationListAPI

urlpatterns = [
    path('citation-generator/', CitationPage.as_view(), name='citations'),
    path('api/citations/generate/', GenerateCitationAPI.as_view(), name='citations_generate'),
    path('api/citations/autocite/', AutociteAPI.as_view(), name='citations_autocite'),
    path('api/citations/lists/', CitationListAPI.as_view(), name='citations_lists'),
]
