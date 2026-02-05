from django.contrib import admin
from summarizer.models import SummaryHistory


@admin.register(SummaryHistory)
class SummaryHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mode', 'summary_length', 'word_count', 'created_at')
    list_filter = ('mode', 'created_at')
    search_fields = ('user__email', 'input_text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
