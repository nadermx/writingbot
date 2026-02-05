from django.conf import settings
from django.db import models
from django.utils import timezone


class GenerationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_tool_generations',
    )
    tool_slug = models.CharField(max_length=100, db_index=True)
    input_params = models.JSONField(default=dict)
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Generation History'
        verbose_name_plural = 'Generation Histories'

    def __str__(self):
        return f'{self.tool_slug} - {self.created_at:%Y-%m-%d %H:%M}'


class DailyUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_tool_daily_usage',
    )
    ip_hash = models.CharField(max_length=64, blank=True, default='')
    date = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            ('user', 'date'),
            ('ip_hash', 'date'),
        ]
        verbose_name = 'Daily Usage'
        verbose_name_plural = 'Daily Usages'

    def __str__(self):
        identifier = self.user.email if self.user else self.ip_hash[:12]
        return f'{identifier} - {self.date} - {self.count} uses'
