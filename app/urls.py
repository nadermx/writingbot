from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

import config

admin.site.site_title = f"{config.PROJECT_NAME} Admin"
admin.site.site_header = f"{config.PROJECT_NAME} Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),

    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),

    # Payment webhooks
    path('ipns/', include('finances.urls.payment')),

    # Captcha
    path('captcha/', include('captcha.urls')),

    # Tool apps
    path('', include('paraphraser.urls')),
    path('', include('grammar.urls')),
    path('', include('summarizer.urls')),
    path('', include('ai_detector.urls')),
    path('', include('humanizer.urls')),
    path('', include('plagiarism.urls')),
    path('', include('translator.urls')),
    path('', include('citations.urls')),
    path('', include('flow.urls')),
    path('', include('ai_tools.urls')),
    path('', include('word_counter.urls')),
    path('', include('pdf_tools.urls')),
    path('', include('media_tools.urls')),
    path('', include('seo.urls')),
    path('', include('courses.urls')),
    path('', include('blog.urls')),

    # Core pages (catch-all, must be last)
    path('', include('core.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
