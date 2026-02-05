from django.db import models
from django.conf import settings


class TranslationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='translation_history'
    )
    input_text = models.TextField()
    output_text = models.TextField()
    source_lang = models.CharField(max_length=10, help_text='Source language code')
    target_lang = models.CharField(max_length=10, help_text='Target language code')
    char_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Translation History'
        verbose_name_plural = 'Translation History'

    def __str__(self):
        return f'{self.source_lang} -> {self.target_lang} ({self.char_count} chars)'
