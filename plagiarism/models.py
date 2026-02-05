from django.db import models
from django.conf import settings
from django.utils import timezone


class PlagiarismReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plagiarism_reports'
    )
    input_text = models.TextField()
    similarity_percentage = models.FloatField(default=0.0)
    word_count = models.IntegerField(default=0)
    matches = models.JSONField(
        default=list,
        blank=True,
        help_text='List of matches: [{source_url, matched_text, similarity_percent, title}]'
    )
    words_used_this_month = models.IntegerField(
        default=0,
        help_text='Snapshot of words used this month at time of check'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Plagiarism Report'
        verbose_name_plural = 'Plagiarism Reports'

    def __str__(self):
        return f'{self.user.email} - {self.similarity_percentage}% ({self.word_count} words) - {self.created_at:%Y-%m-%d %H:%M}'


class PlagiarismUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plagiarism_usage'
    )
    month = models.DateField(
        help_text='First day of the month for tracking (YYYY-MM-01)'
    )
    words_used = models.IntegerField(default=0)

    class Meta:
        ordering = ['-month']
        unique_together = ('user', 'month')
        verbose_name = 'Plagiarism Usage'
        verbose_name_plural = 'Plagiarism Usage'

    def __str__(self):
        return f'{self.user.email} - {self.month:%Y-%m} - {self.words_used} words'
