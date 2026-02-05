from django.urls import path

from flow.views import (
    FlowPage,
    SharedDocumentPage,
    DocumentListAPI,
    DocumentDetailAPI,
    AISuggestAPI,
    AIReviewAPI,
    SmartStartAPI,
    ShareDocumentAPI,
    AIChatPage,
    AIChatAPI,
    AISearchPage,
    AISearchAPI,
)

urlpatterns = [
    # Page routes
    path('flow/', FlowPage.as_view(), name='flow'),
    path('flow/shared/<str:token>/', SharedDocumentPage.as_view(), name='flow_shared'),
    path('ai-chat/', AIChatPage.as_view(), name='ai_chat'),
    path('ai-search/', AISearchPage.as_view(), name='ai_search'),

    # API routes
    path('api/flow/documents/', DocumentListAPI.as_view(), name='flow_documents_api'),
    path('api/flow/documents/<uuid:uuid>/', DocumentDetailAPI.as_view(), name='flow_document_detail_api'),
    path('api/flow/ai-suggest/', AISuggestAPI.as_view(), name='flow_ai_suggest_api'),
    path('api/flow/ai-review/', AIReviewAPI.as_view(), name='flow_ai_review_api'),
    path('api/flow/smart-start/', SmartStartAPI.as_view(), name='flow_smart_start_api'),
    path('api/flow/share/', ShareDocumentAPI.as_view(), name='flow_share_api'),
    path('api/ai-chat/', AIChatAPI.as_view(), name='ai_chat_api'),
    path('api/ai-search/', AISearchAPI.as_view(), name='ai_search_api'),
]
