from django.contrib import admin

from courses.models import Course, Chapter


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ('title', 'slug', 'order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'chapters_count', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('chapters_count', 'created_at')
    inlines = [ChapterInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Stats', {
            'fields': ('chapters_count', 'created_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('course', 'order')

    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'slug', 'order')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )
