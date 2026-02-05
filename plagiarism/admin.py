from django.contrib import admin
from plagiarism.models import PlagiarismReport, PlagiarismUsage


@admin.register(PlagiarismReport)
class PlagiarismReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'similarity_percentage', 'word_count', 'words_used_this_month', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    raw_id_fields = ('user',)
    readonly_fields = ('input_text', 'matches', 'similarity_percentage', 'word_count', 'words_used_this_month')


@admin.register(PlagiarismUsage)
class PlagiarismUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'words_used')
    list_filter = ('month',)
    search_fields = ('user__email',)
    raw_id_fields = ('user',)
