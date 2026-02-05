import logging

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from accounts.views import GlobalVars
from blog.models import Category, Post, Tag
import config

logger = logging.getLogger('app')

POSTS_PER_PAGE = 12


class BlogIndex(View):
    """Blog listing page with featured post, categories, and pagination."""

    def get(self, request):
        g = GlobalVars.get_globals(request)

        posts_qs = Post.objects.filter(is_published=True).select_related('author', 'category')
        featured_post = posts_qs.first()

        # Exclude featured post from main list
        if featured_post:
            list_qs = posts_qs.exclude(pk=featured_post.pk)
        else:
            list_qs = posts_qs

        paginator = Paginator(list_qs, POSTS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        tags = Tag.objects.all()[:20]

        return render(request, 'blog/index.html', {
            'title': f'Blog | {config.PROJECT_NAME}',
            'description': f'Writing tips, AI tools guides, and productivity articles from {config.PROJECT_NAME}.',
            'page': 'blog',
            'g': g,
            'featured_post': featured_post,
            'posts': page_obj,
            'categories': categories,
            'tags': tags,
        })


class BlogPost(View):
    """Individual blog post page."""

    def get(self, request, slug):
        g = GlobalVars.get_globals(request)
        post = get_object_or_404(Post, slug=slug, is_published=True)

        # Increment view count
        post.increment_views()

        # Related posts: same category, excluding current
        related_posts = Post.objects.filter(
            is_published=True, category=post.category
        ).exclude(pk=post.pk)[:4] if post.category else Post.objects.none()

        categories = Category.objects.all()
        tags = Tag.objects.all()[:20]

        return render(request, 'blog/post.html', {
            'title': f'{post.title} | {config.PROJECT_NAME}',
            'description': post.meta_description or post.excerpt[:160],
            'page': 'blog',
            'g': g,
            'post': post,
            'related_posts': related_posts,
            'categories': categories,
            'tags': tags,
        })


class BlogCategory(View):
    """Blog posts filtered by category."""

    def get(self, request, slug):
        g = GlobalVars.get_globals(request)
        category = get_object_or_404(Category, slug=slug)

        posts_qs = Post.objects.filter(
            is_published=True, category=category
        ).select_related('author', 'category')

        paginator = Paginator(posts_qs, POSTS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        tags = Tag.objects.all()[:20]

        return render(request, 'blog/index.html', {
            'title': f'{category.name} - Blog | {config.PROJECT_NAME}',
            'description': category.description or f'Articles about {category.name}.',
            'page': 'blog',
            'g': g,
            'posts': page_obj,
            'current_category': category,
            'categories': categories,
            'tags': tags,
        })


class BlogTag(View):
    """Blog posts filtered by tag."""

    def get(self, request, slug):
        g = GlobalVars.get_globals(request)
        tag = get_object_or_404(Tag, slug=slug)

        posts_qs = Post.objects.filter(
            is_published=True, tags=tag
        ).select_related('author', 'category')

        paginator = Paginator(posts_qs, POSTS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        tags_list = Tag.objects.all()[:20]

        return render(request, 'blog/index.html', {
            'title': f'#{tag.name} - Blog | {config.PROJECT_NAME}',
            'description': f'Articles tagged with {tag.name}.',
            'page': 'blog',
            'g': g,
            'posts': page_obj,
            'current_tag': tag,
            'categories': categories,
            'tags': tags_list,
        })
