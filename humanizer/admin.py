from django.contrib import admin
from humanizer.models import HumanizeHistory


@admin.register(HumanizeHistory)
class HumanizeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mode', 'ai_score_before', 'ai_score_after', 'created_at')
    list_filter = ('mode', 'created_at')
    search_fields = ('input_text', 'output_text', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
