from django.urls import path

from ai_tools.views import AIToolsIndexPage, AIToolPage, AIToolGenerateAPI

urlpatterns = [
    # Index page listing all AI tools
    path('ai-writing-tools/', AIToolsIndexPage.as_view(), name='ai_tools_index'),

    # API endpoint for generation
    path('api/ai-tools/generate/', AIToolGenerateAPI.as_view(), name='ai_tools_generate_api'),

    # Individual tool pages (must be last - catch-all slug pattern)
    path('ai-writing-tools/<slug:slug>/', AIToolPage.as_view(), name='ai_tool_page'),
]
