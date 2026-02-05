import logging

from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from accounts.views import GlobalVars
from courses.models import Course, Chapter
import config

logger = logging.getLogger('app')


class CoursesIndex(View):
    """Course listing page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        courses = Course.objects.filter(is_published=True)

        # Group by category
        categories = {}
        for course in courses:
            cat = course.category or 'General'
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(course)

        return render(request, 'courses/index.html', {
            'title': f'Free Writing Courses | {config.PROJECT_NAME}',
            'description': 'Free online courses to improve your writing skills. Learn grammar, essay writing, academic writing, and more.',
            'page': 'courses',
            'g': g,
            'courses': courses,
            'categories': categories,
        })


class CourseDetail(View):
    """Course detail page with chapter listing."""

    def get(self, request, slug):
        g = GlobalVars.get_globals(request)
        course = get_object_or_404(Course, slug=slug, is_published=True)
        chapters = course.chapters.all()

        return render(request, 'courses/course.html', {
            'title': f'{course.title} | {config.PROJECT_NAME}',
            'description': course.description[:160] if course.description else f'Learn {course.title} with our free online course.',
            'page': 'courses',
            'g': g,
            'course': course,
            'chapters': chapters,
        })


class ChapterDetail(View):
    """Individual chapter page with content and navigation."""

    def get(self, request, course_slug, chapter_slug):
        g = GlobalVars.get_globals(request)
        course = get_object_or_404(Course, slug=course_slug, is_published=True)
        chapter = get_object_or_404(Chapter, course=course, slug=chapter_slug)

        all_chapters = list(course.chapters.all())
        current_index = None
        for i, ch in enumerate(all_chapters):
            if ch.pk == chapter.pk:
                current_index = i
                break

        return render(request, 'courses/chapter.html', {
            'title': f'{chapter.title} - {course.title} | {config.PROJECT_NAME}',
            'description': f'{chapter.title} from the course {course.title}.',
            'page': 'courses',
            'g': g,
            'course': course,
            'chapter': chapter,
            'chapters': all_chapters,
            'current_index': current_index,
            'total_chapters': len(all_chapters),
        })
