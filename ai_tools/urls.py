from django.urls import path

from ai_tools.views import (
    AIToolsIndex, AIToolPage, AIToolGenerateAPI, AIToolsListAPI,
)

urlpatterns = [
    # Index page listing all AI tools
    path('ai-tools/', AIToolsIndex.as_view(), name='ai_tools_index'),

    # API endpoints
    path('api/ai-tools/', AIToolsListAPI.as_view(), name='ai_tools_list_api'),
    path('api/ai-tools/generate/', AIToolGenerateAPI.as_view(), name='ai_tools_generate_api'),

    # Individual tool pages (must be last - catch-all pattern)
    path('ai-tools/<slug:tool_slug>/', AIToolPage.as_view(), name='ai_tool_page'),
]
