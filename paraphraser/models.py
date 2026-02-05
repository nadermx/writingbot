from django.db import models
from django.conf import settings


class ParaphraseHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paraphrase_history'
    )
    input_text = models.TextField()
    output_text = models.TextField()
    mode = models.CharField(max_length=50, default='standard')
    synonym_level = models.IntegerField(default=3, help_text='Synonym intensity from 1 (minimal) to 5 (maximum)')
    frozen_words = models.JSONField(default=list, blank=True, help_text='Words locked from paraphrasing')
    settings = models.JSONField(default=dict, blank=True, help_text='Additional settings (contractions, active voice, etc.)')
    language = models.CharField(max_length=10, default='en')
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Paraphrase History'
        verbose_name_plural = 'Paraphrase History'

    def __str__(self):
        preview = self.input_text[:80] + '...' if len(self.input_text) > 80 else self.input_text
        return f'{self.user.email} - {self.mode} - {preview}'
