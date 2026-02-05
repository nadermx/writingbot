from django.contrib import admin

from ai_tools.models import GenerationHistory, DailyUsage


@admin.register(GenerationHistory)
class GenerationHistoryAdmin(admin.ModelAdmin):
    list_display = ('tool_slug', 'user', 'created_at')
    list_filter = ('tool_slug', 'created_at')
    search_fields = ('tool_slug', 'user__email')
    readonly_fields = ('user', 'tool_slug', 'input_params', 'output_text', 'created_at')
    ordering = ('-created_at',)


@admin.register(DailyUsage)
class DailyUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_hash', 'date', 'count')
    list_filter = ('date',)
    search_fields = ('user__email', 'ip_hash')
    ordering = ('-date',)
