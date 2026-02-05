import uuid as uuid_lib

from django.conf import settings
from django.db import models


class Document(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='flow_documents'
    )
    title = models.CharField(max_length=500, default='Untitled Document')
    content = models.TextField(blank=True, default='', help_text='Stores HTML content from the editor')
    uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True, editable=False)
    is_shared = models.BooleanField(default=False)
    share_token = models.CharField(max_length=64, null=True, blank=True, unique=True)
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f'{self.user.email} - {self.title}'


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    content = models.TextField(blank=True, default='')
    version_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version_number']
        verbose_name = 'Document Version'
        verbose_name_plural = 'Document Versions'
        unique_together = ['document', 'version_number']

    def __str__(self):
        return f'{self.document.title} - v{self.version_number}'


class Note(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    content = models.TextField(blank=True, default='')
    position = models.IntegerField(default=0, help_text='Ordering position')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        preview = self.content[:80] + '...' if len(self.content) > 80 else self.content
        return f'{self.document.title} - Note: {preview}'
