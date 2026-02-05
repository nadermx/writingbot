from django.urls import path

from blog.views import BlogIndex, BlogPost, BlogCategory, BlogTag

urlpatterns = [
    path('blog/', BlogIndex.as_view(), name='blog_index'),
    path('blog/category/<slug:slug>/', BlogCategory.as_view(), name='blog_category'),
    path('blog/tag/<slug:slug>/', BlogTag.as_view(), name='blog_tag'),
    path('blog/<slug:slug>/', BlogPost.as_view(), name='blog_post'),
]
