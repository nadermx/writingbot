from django.db import models
from django.conf import settings


class DetectionResult(models.Model):
    CLASSIFICATION_CHOICES = [
        ('ai_generated', 'AI Generated'),
        ('ai_refined', 'AI Refined'),
        ('human_refined', 'Human Refined'),
        ('human_written', 'Human Written'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='detection_results'
    )
    input_text = models.TextField()
    results = models.JSONField(default=dict, help_text='Sentence-level scores and labels')
    overall_score = models.FloatField(default=0.0, help_text='0-100, where 100 = fully AI generated')
    classification = models.CharField(
        max_length=20,
        choices=CLASSIFICATION_CHOICES,
        default='human_written'
    )
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Detection Result'
        verbose_name_plural = 'Detection Results'

    def __str__(self):
        return f'{self.classification} ({self.overall_score}%) - {self.word_count} words'
