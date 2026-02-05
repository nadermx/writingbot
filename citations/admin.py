from django.contrib import admin
from citations.models import CitationStyle, CitationList, Citation


@admin.register(CitationStyle)
class CitationStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(CitationList)
class CitationListAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'style', 'created_at', 'updated_at')
    list_filter = ('style', 'created_at')
    search_fields = ('user__email', 'name')
    raw_id_fields = ('user',)


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ('citation_list', 'source_type', 'get_title', 'created_at')
    list_filter = ('source_type', 'created_at')
    search_fields = ('formatted_text', 'citation_list__user__email')
    raw_id_fields = ('citation_list',)

    def get_title(self, obj):
        return obj.metadata.get('title', 'Untitled')[:60]
    get_title.short_description = 'Title'
