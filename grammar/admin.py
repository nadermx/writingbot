from django.contrib import admin
from grammar.models import GrammarCheckHistory


@admin.register(GrammarCheckHistory)
class GrammarCheckHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'word_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'input_text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
