from django.urls import path

from media_tools.views import (
    MediaToolsIndex, ImageConverterPage, BackgroundRemoverPage,
    AIImageGeneratorPage, QRCodePage, VoiceGeneratorPage,
    TranscriptionPage, LogoGeneratorPage, CharacterGeneratorPage,
    WordCloudPage, BannerGeneratorPage, PresentationMakerPage,
    ImageConvertAPI, BackgroundRemoveAPI, QRCodeAPI,
    VoiceGenerateAPI, AIImagePromptAPI,
    TranscribeAPI, LogoGenerateAPI, CharacterGenerateAPI,
    WordCloudAPI, BannerGenerateAPI, PresentationGenerateAPI,
)

urlpatterns = [
    # Page views
    path('image-tools/', AIImageGeneratorPage.as_view(), name='ai_image_generator'),
    path('converter-tools/', ImageConverterPage.as_view(), name='image_converter'),
    path('background-remover/', BackgroundRemoverPage.as_view(), name='background_remover'),
    path('tools/qr-code-generator/', QRCodePage.as_view(), name='qr_code_generator'),
    path('tools/ai-voice-generator/', VoiceGeneratorPage.as_view(), name='voice_generator'),
    path('tools/transcription/', TranscriptionPage.as_view(), name='transcription'),
    path('speech-to-text/', TranscriptionPage.as_view(), name='speech_to_text'),
    path('tools/logo-generator/', LogoGeneratorPage.as_view(), name='logo_generator'),
    path('tools/character-generator/', CharacterGeneratorPage.as_view(), name='character_generator'),
    path('tools/word-cloud/', WordCloudPage.as_view(), name='word_cloud'),
    path('tools/banner-generator/', BannerGeneratorPage.as_view(), name='banner_generator'),
    path('tools/presentation-maker/', PresentationMakerPage.as_view(), name='presentation_maker'),
    path('media-tools/', MediaToolsIndex.as_view(), name='media_tools_index'),

    # API endpoints
    path('api/media/convert-image/', ImageConvertAPI.as_view(), name='image_convert_api'),
    path('api/media/remove-bg/', BackgroundRemoveAPI.as_view(), name='bg_remove_api'),
    path('api/media/qr-code/', QRCodeAPI.as_view(), name='qr_code_api'),
    path('api/media/text-to-speech/', VoiceGenerateAPI.as_view(), name='voice_api'),
    path('api/media/ai-image/', AIImagePromptAPI.as_view(), name='ai_image_api'),
    path('api/media/transcribe/', TranscribeAPI.as_view(), name='transcribe_api'),
    path('api/media/logo/', LogoGenerateAPI.as_view(), name='logo_api'),
    path('api/media/character/', CharacterGenerateAPI.as_view(), name='character_api'),
    path('api/media/word-cloud/', WordCloudAPI.as_view(), name='word_cloud_api'),
    path('api/media/banner/', BannerGenerateAPI.as_view(), name='banner_api'),
    path('api/media/presentation/', PresentationGenerateAPI.as_view(), name='presentation_api'),
]
