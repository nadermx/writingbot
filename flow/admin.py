from django.contrib import admin

from flow.models import Document, DocumentVersion, Note


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'word_count', 'is_shared', 'created_at', 'updated_at')
    list_filter = ('is_shared', 'created_at', 'updated_at')
    search_fields = ('user__email', 'title', 'content')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('document__title',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('document', 'position', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('document__title', 'content')
    readonly_fields = ('created_at',)
    ordering = ('document', 'position')
