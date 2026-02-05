from django.urls import path

from courses.views import CoursesIndex, CourseDetail, ChapterDetail

urlpatterns = [
    path('courses/', CoursesIndex.as_view(), name='courses_index'),
    path('courses/<slug:slug>/', CourseDetail.as_view(), name='course_detail'),
    path('courses/<slug:course_slug>/<slug:chapter_slug>/', ChapterDetail.as_view(), name='chapter_detail'),
]
