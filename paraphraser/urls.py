from django.urls import path

from paraphraser.views import ParaphraserPage, ParaphraseAPI, SynonymAPI, HistoryAPI

urlpatterns = [
    path('paraphrasing-tool/', ParaphraserPage.as_view(), name='paraphraser'),
    path('api/paraphrase/', ParaphraseAPI.as_view(), name='paraphrase_api'),
    path('api/paraphrase/synonyms/', SynonymAPI.as_view(), name='paraphrase_synonyms_api'),
    path('api/paraphrase/history/', HistoryAPI.as_view(), name='paraphrase_history_api'),
]
