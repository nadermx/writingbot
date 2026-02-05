from django.db import models
from django.conf import settings


class HumanizeHistory(models.Model):
    MODE_CHOICES = [
        ('basic', 'Basic'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='humanize_history'
    )
    input_text = models.TextField()
    output_text = models.TextField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='basic')
    ai_score_before = models.FloatField(default=0.0, help_text='AI score before humanization (0-100)')
    ai_score_after = models.FloatField(default=0.0, help_text='AI score after humanization (0-100)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Humanize History'
        verbose_name_plural = 'Humanize History'

    def __str__(self):
        return f'{self.mode} - {self.ai_score_before}% -> {self.ai_score_after}%'
