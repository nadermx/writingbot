import logging
import re
import secrets

from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from app.utils import Utils
from flow.models import Document, DocumentVersion, Note
from flow.services import FlowService
import config

logger = logging.getLogger('app')


def strip_html(html):
    """Strip HTML tags and return plain text."""
    if not html:
        return ''
    return re.sub(r'<[^>]+>', ' ', html).strip()


def count_words(text):
    """Count words in a plain text string."""
    text = strip_html(text)
    if not text or not text.strip():
        return 0
    return len(text.split())


class FlowPage(View):
    """Renders the main Flow co-writer editor page. Freemium — anonymous users get daily limits."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = request.user.is_authenticated and request.user.is_plan_active

        return render(
            request,
            'flow/editor.html',
            {
                'title': f"Flow - Co-Writer | {config.PROJECT_NAME}",
                'description': 'AI-powered writing workspace. Write, research, and collaborate with AI assistance.',
                'page': 'flow',
                'g': g,
                'is_premium': is_premium,
                'is_authenticated': request.user.is_authenticated,
            }
        )


class DocumentListAPI(APIView):
    """
    GET  /api/flow/documents/  - List user's documents
    POST /api/flow/documents/  - Create a new document
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        documents = Document.objects.filter(user=request.user).order_by('-updated_at')
        return Response({
            'documents': [
                {
                    'uuid': str(doc.uuid),
                    'title': doc.title,
                    'word_count': doc.word_count,
                    'is_shared': doc.is_shared,
                    'created_at': doc.created_at.isoformat(),
                    'updated_at': doc.updated_at.isoformat(),
                }
                for doc in documents
            ]
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data
        title = data.get('title', 'Untitled Document').strip()
        content = data.get('content', '')

        doc = Document.objects.create(
            user=request.user,
            title=title or 'Untitled Document',
            content=content,
            word_count=count_words(content),
        )

        return Response({
            'uuid': str(doc.uuid),
            'title': doc.title,
            'content': doc.content,
            'word_count': doc.word_count,
            'is_shared': doc.is_shared,
            'created_at': doc.created_at.isoformat(),
            'updated_at': doc.updated_at.isoformat(),
        }, status=status.HTTP_201_CREATED)


class DocumentDetailAPI(APIView):
    """
    GET    /api/flow/documents/<uuid>/  - Retrieve a document
    PUT    /api/flow/documents/<uuid>/  - Update a document
    DELETE /api/flow/documents/<uuid>/  - Delete a document
    """

    def get(self, request, uuid):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        doc = get_object_or_404(Document, uuid=uuid, user=request.user)
        notes = Note.objects.filter(document=doc).order_by('position')

        return Response({
            'uuid': str(doc.uuid),
            'title': doc.title,
            'content': doc.content,
            'word_count': doc.word_count,
            'is_shared': doc.is_shared,
            'share_token': doc.share_token,
            'created_at': doc.created_at.isoformat(),
            'updated_at': doc.updated_at.isoformat(),
            'notes': [
                {
                    'id': note.id,
                    'content': note.content,
                    'position': note.position,
                    'created_at': note.created_at.isoformat(),
                }
                for note in notes
            ],
        })

    def put(self, request, uuid):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        doc = get_object_or_404(Document, uuid=uuid, user=request.user)
        data = request.data

        # Save a version snapshot before updating (if content changed substantially)
        old_word_count = doc.word_count
        new_content = data.get('content', doc.content)
        new_word_count = count_words(new_content)

        if doc.content and abs(new_word_count - old_word_count) > 50:
            last_version = doc.versions.first()
            next_version = (last_version.version_number + 1) if last_version else 1
            DocumentVersion.objects.create(
                document=doc,
                content=doc.content,
                version_number=next_version,
            )

        # Update document fields
        if 'title' in data:
            doc.title = data['title'].strip() or 'Untitled Document'
        if 'content' in data:
            doc.content = new_content
            doc.word_count = new_word_count

        # Handle notes if provided
        if 'notes' in data:
            note_list = data['notes']
            # Delete existing notes and recreate
            doc.notes.all().delete()
            for i, note_data in enumerate(note_list):
                if isinstance(note_data, dict):
                    Note.objects.create(
                        document=doc,
                        content=note_data.get('content', ''),
                        position=i,
                    )
                elif isinstance(note_data, str):
                    Note.objects.create(
                        document=doc,
                        content=note_data,
                        position=i,
                    )

        doc.save()

        return Response({
            'uuid': str(doc.uuid),
            'title': doc.title,
            'word_count': doc.word_count,
            'updated_at': doc.updated_at.isoformat(),
        })

    def delete(self, request, uuid):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        doc = get_object_or_404(Document, uuid=uuid, user=request.user)
        doc.delete()

        return Response({'success': True}, status=status.HTTP_200_OK)


class AISuggestAPI(APIView):
    """
    POST /api/flow/ai-suggest/
    Get AI-generated next sentence suggestions based on document content.
    """

    def post(self, request):
        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'flow_suggest', request.user, ip, user_agent,
        )

        if not allowed:
            return Response(
                {
                    'error': f'Daily limit of {limit} suggestions reached. Upgrade to Premium for unlimited access.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        content = data.get('content', '').strip()
        cursor_position = data.get('cursor_position')

        # Strip HTML for the AI
        plain_text = strip_html(content)

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        suggestion, error = FlowService.suggest_next(plain_text, cursor_position, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        FlowService.increment_daily_usage('flow_suggest', request.user, ip, user_agent)

        return Response({
            'suggestion': suggestion,
        })


class AIReviewAPI(APIView):
    """
    POST /api/flow/ai-review/
    Get AI review/feedback on a document.
    """

    def post(self, request):
        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'flow_review', request.user, ip, user_agent,
        )

        if not allowed:
            return Response(
                {
                    'error': f'Daily limit of {limit} reviews reached. Upgrade to Premium for unlimited access.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        content = data.get('content', '').strip()

        # Strip HTML for the AI
        plain_text = strip_html(content)

        if not plain_text:
            return Response(
                {'error': 'Please write some content before requesting a review.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        review, error = FlowService.ai_review(plain_text, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        FlowService.increment_daily_usage('flow_review', request.user, ip, user_agent)

        return Response({
            'review': review,
        })


class SmartStartAPI(APIView):
    """
    POST /api/flow/smart-start/
    Generate a document outline from keywords.
    """

    def post(self, request):
        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'flow_smart_start', request.user, ip, user_agent,
        )

        if not allowed:
            return Response(
                {
                    'error': f'Daily limit of {limit} outlines reached. Upgrade to Premium for unlimited access.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        keywords = data.get('keywords', '').strip()

        if not keywords:
            return Response(
                {'error': 'Please provide keywords or a topic.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        outline, error = FlowService.smart_start(keywords, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        FlowService.increment_daily_usage('flow_smart_start', request.user, ip, user_agent)

        return Response({
            'outline': outline,
        })


class ShareDocumentAPI(APIView):
    """
    POST /api/flow/share/
    Generate or toggle a share link for a document.
    """

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data
        doc_uuid = data.get('uuid')

        if not doc_uuid:
            return Response(
                {'error': 'Document UUID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc = get_object_or_404(Document, uuid=doc_uuid, user=request.user)

        # Toggle sharing
        if doc.is_shared:
            # Disable sharing
            doc.is_shared = False
            doc.share_token = None
            doc.save()
            return Response({
                'is_shared': False,
                'share_url': None,
            })
        else:
            # Enable sharing
            doc.is_shared = True
            doc.share_token = secrets.token_urlsafe(32)
            doc.save()
            share_url = f'{config.ROOT_DOMAIN}/flow/shared/{doc.share_token}/'
            return Response({
                'is_shared': True,
                'share_url': share_url,
                'share_token': doc.share_token,
            })


class SharedDocumentPage(View):
    """Public view for shared documents (no auth required)."""

    def get(self, request, token):
        g = GlobalVars.get_globals(request)
        doc = get_object_or_404(Document, share_token=token, is_shared=True)

        return render(
            request,
            'flow/editor.html',
            {
                'title': f"{doc.title} | {config.PROJECT_NAME}",
                'description': f'Shared document: {doc.title}',
                'page': 'flow_shared',
                'g': g,
                'is_premium': False,
                'shared_document': {
                    'title': doc.title,
                    'content': doc.content,
                    'word_count': doc.word_count,
                    'created_at': doc.created_at.isoformat(),
                    'updated_at': doc.updated_at.isoformat(),
                },
                'is_shared_view': True,
            }
        )


# ======================================================================
# AI Chat
# ======================================================================

class AIChatPage(View):
    """GET /ai-chat/ - Renders the AI Chat page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )

        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'ai_chat', request.user, ip, user_agent,
        )

        return render(
            request,
            'tools/ai-chat.html',
            {
                'title': f'AI Chat | {config.PROJECT_NAME}',
                'description': 'Chat with an AI writing assistant. Get help with brainstorming, grammar, outlines, and more.',
                'page': 'ai-chat',
                'g': g,
                'is_premium': is_premium,
                'remaining': remaining,
                'limit': limit,
            }
        )


class AIChatAPI(APIView):
    """POST /api/ai-chat/ - Send a message and get an AI response."""

    def post(self, request):
        message = request.data.get('message', '').strip()
        history = request.data.get('history', [])

        if not message:
            return Response(
                {'error': 'Please enter a message.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Rate limiting
        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'ai_chat', request.user, ip, user_agent,
        )

        if not allowed:
            return Response(
                {
                    'error': f'Daily limit of {limit} messages reached. Upgrade to Premium for unlimited chat.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Call the chat service
        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        reply, error = FlowService.chat(message, history, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Increment usage counter
        FlowService.increment_daily_usage('ai_chat', request.user, ip, user_agent)

        # Re-check remaining
        _, remaining, limit = FlowService.check_daily_limit(
            'ai_chat', request.user, ip, user_agent,
        )

        return Response({
            'reply': reply,
            'remaining': remaining,
            'limit': limit,
        })


# ======================================================================
# AI Search
# ======================================================================

class AISearchPage(View):
    """GET /ai-search/ - Renders the AI Search page."""

    def get(self, request):
        g = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )

        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'ai_search', request.user, ip, user_agent,
        )

        return render(
            request,
            'tools/ai-search.html',
            {
                'title': f'AI Search | {config.PROJECT_NAME}',
                'description': 'AI-powered research search. Get comprehensive, synthesized answers to your questions with source references.',
                'page': 'ai-search',
                'g': g,
                'is_premium': is_premium,
                'remaining': remaining,
                'limit': limit,
            }
        )


class AISearchAPI(APIView):
    """POST /api/ai-search/ - Perform an AI-powered search."""

    def post(self, request):
        query = request.data.get('query', '').strip()

        if not query:
            return Response(
                {'error': 'Please enter a search query.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Rate limiting
        ip = Utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        allowed, remaining, limit = FlowService.check_daily_limit(
            'ai_search', request.user, ip, user_agent,
        )

        if not allowed:
            return Response(
                {
                    'error': f'Daily limit of {limit} searches reached. Upgrade to Premium for unlimited searches.',
                    'upgrade': True,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Call the search service
        is_premium = (
            request.user.is_authenticated
            and getattr(request.user, 'is_plan_active', False)
        )
        result, error = FlowService.search(query, use_premium=is_premium)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Increment usage counter
        FlowService.increment_daily_usage('ai_search', request.user, ip, user_agent)

        # Re-check remaining
        _, remaining, limit = FlowService.check_daily_limit(
            'ai_search', request.user, ip, user_agent,
        )

        return Response({
            'answer': result['answer'],
            'sources': result['sources'],
            'remaining': remaining,
            'limit': limit,
        })
