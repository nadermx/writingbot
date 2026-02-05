from django.db import models
from django.conf import settings


class SummaryHistory(models.Model):
    MODE_CHOICES = [
        ('key_sentences', 'Key Sentences'),
        ('paragraph', 'Paragraph'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='summaries'
    )
    input_text = models.TextField()
    output_text = models.TextField(blank=True, default='')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='paragraph')
    summary_length = models.IntegerField(default=3, help_text='Length setting 1 (shortest) to 5 (longest)')
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Summary'
        verbose_name_plural = 'Summaries'

    def __str__(self):
        return f"Summary ({self.mode}, {self.word_count} words) - {self.created_at:%Y-%m-%d %H:%M}"
