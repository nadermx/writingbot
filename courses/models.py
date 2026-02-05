from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=200, blank=True, default='')
    chapters_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-update chapters count
        if self.pk:
            self.chapters_count = self.chapters.count()
        super().save(*args, **kwargs)

    def update_chapter_count(self):
        """Update the chapters_count field based on actual chapters."""
        self.chapters_count = self.chapters.count()
        self.save(update_fields=['chapters_count'])

    @property
    def published_chapters(self):
        return self.chapters.all()

    @property
    def first_chapter(self):
        return self.chapters.first()


class Chapter(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='chapters',
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, blank=True)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = [('course', 'slug')]

    def __str__(self):
        return f'{self.course.title} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Update course chapter count
        if self.course_id:
            self.course.update_chapter_count()

    @property
    def next_chapter(self):
        return Chapter.objects.filter(
            course=self.course,
            order__gt=self.order,
        ).first()

    @property
    def previous_chapter(self):
        return Chapter.objects.filter(
            course=self.course,
            order__lt=self.order,
        ).order_by('-order').first()

    @property
    def reading_time(self):
        """Estimated reading time in minutes."""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))
