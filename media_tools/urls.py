from django.urls import path

from media_tools.views import (
    MediaToolsIndex, ImageConverterPage, BackgroundRemoverPage,
    AIImageGeneratorPage, QRCodePage, VoiceGeneratorPage,
    ImageConvertAPI, BackgroundRemoveAPI, QRCodeAPI,
    VoiceGenerateAPI, AIImagePromptAPI,
)

urlpatterns = [
    # Page views
    path('image-tools/', ImageConverterPage.as_view(), name='image_converter'),
    path('converter-tools/', AIImageGeneratorPage.as_view(), name='ai_image_generator'),
    path('background-remover/', BackgroundRemoverPage.as_view(), name='background_remover'),
    path('tools/qr-code-generator/', QRCodePage.as_view(), name='qr_code_generator'),
    path('tools/ai-voice-generator/', VoiceGeneratorPage.as_view(), name='voice_generator'),
    path('media-tools/', MediaToolsIndex.as_view(), name='media_tools_index'),

    # API endpoints
    path('api/media/convert-image/', ImageConvertAPI.as_view(), name='image_convert_api'),
    path('api/media/remove-bg/', BackgroundRemoveAPI.as_view(), name='bg_remove_api'),
    path('api/media/qr-code/', QRCodeAPI.as_view(), name='qr_code_api'),
    path('api/media/text-to-speech/', VoiceGenerateAPI.as_view(), name='voice_api'),
    path('api/media/ai-image/', AIImagePromptAPI.as_view(), name='ai_image_api'),
]
