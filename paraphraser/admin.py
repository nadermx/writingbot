from django.contrib import admin

from paraphraser.models import ParaphraseHistory


@admin.register(ParaphraseHistory)
class ParaphraseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mode', 'synonym_level', 'word_count', 'language', 'created_at')
    list_filter = ('mode', 'language', 'created_at')
    search_fields = ('user__email', 'input_text', 'output_text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
