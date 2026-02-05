from django.contrib import admin
from ai_detector.models import DetectionResult


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'classification', 'overall_score', 'word_count', 'created_at')
    list_filter = ('classification', 'created_at')
    search_fields = ('input_text', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
