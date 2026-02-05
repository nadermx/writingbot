from django.contrib import admin
from translator.models import TranslationHistory


@admin.register(TranslationHistory)
class TranslationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'source_lang', 'target_lang', 'char_count', 'created_at')
    list_filter = ('source_lang', 'target_lang', 'created_at')
    search_fields = ('input_text', 'output_text', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
