from django.db import models
from django.conf import settings


class CitationStyle(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    format_template = models.TextField(
        blank=True,
        help_text='Template string for formatting citations in this style'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Citation Style'
        verbose_name_plural = 'Citation Styles'

    def __str__(self):
        return self.name


class CitationList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citation_lists'
    )
    name = models.CharField(max_length=255, default='My Citations')
    style = models.ForeignKey(
        CitationStyle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citation_lists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Citation List'
        verbose_name_plural = 'Citation Lists'

    def __str__(self):
        return f'{self.user.email} - {self.name}'


class Citation(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('website', 'Website'),
        ('book', 'Book'),
        ('journal', 'Journal'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('article', 'Article'),
    ]

    citation_list = models.ForeignKey(
        CitationList,
        on_delete=models.CASCADE,
        related_name='citations'
    )
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES, default='website')
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Citation metadata: author, title, date, url, publisher, volume, issue, pages, doi, isbn'
    )
    formatted_text = models.TextField(blank=True)
    in_text_citation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Citation'
        verbose_name_plural = 'Citations'

    def __str__(self):
        title = self.metadata.get('title', 'Untitled')
        return f'{self.source_type}: {title[:60]}'
