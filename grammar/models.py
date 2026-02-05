from django.db import models
from django.conf import settings


class GrammarCheckHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='grammar_checks'
    )
    input_text = models.TextField()
    corrections = models.JSONField(default=list, blank=True)
    writing_score = models.JSONField(default=dict, blank=True, help_text='Scores: grammar, fluency, clarity, engagement, delivery (0-100)')
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Grammar Check'
        verbose_name_plural = 'Grammar Checks'

    def __str__(self):
        return f"Grammar check ({self.word_count} words) - {self.created_at:%Y-%m-%d %H:%M}"
