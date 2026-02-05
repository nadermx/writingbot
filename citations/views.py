import logging

from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from citations.models import CitationStyle, CitationList, Citation
from citations.services import CitationService
import config

logger = logging.getLogger('app')


class CitationPage(View):
    """Citation generator page - completely free tool."""

    def get(self, request):
        settings = GlobalVars.get_globals(request)
        styles = CitationService.get_styles()
        return render(
            request,
            'tools/citations.html',
            {
                'title': f"Free Citation Generator | {config.PROJECT_NAME}",
                'description': 'Generate accurate citations in APA, MLA, Chicago, Harvard, IEEE, and more. Free citation generator with autocite.',
                'page': 'citations',
                'g': settings,
                'styles': styles,
            }
        )


class GenerateCitationAPI(APIView):
    """POST - Generate a formatted citation from metadata."""

    def post(self, request):
        data = request.data
        source_type = data.get('source_type', 'website')
        style = data.get('style', 'apa')
        metadata = data.get('metadata', {})

        if not metadata.get('title'):
            return Response(
                {'error': 'A title is required to generate a citation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, error = CitationService.generate_citation(source_type, metadata, style)

        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        # Save to citation list if user is authenticated and list_id provided
        list_id = data.get('list_id')
        if request.user.is_authenticated and list_id:
            try:
                citation_list = CitationList.objects.get(id=list_id, user=request.user)
                Citation.objects.create(
                    citation_list=citation_list,
                    source_type=source_type,
                    metadata=metadata,
                    formatted_text=result['formatted_text'],
                    in_text_citation=result['in_text_citation'],
                )
            except CitationList.DoesNotExist:
                pass

        return Response(result)


class AutociteAPI(APIView):
    """POST - Auto-generate citation metadata from a URL."""

    def post(self, request):
        url = request.data.get('url', '').strip()

        if not url:
            return Response(
                {'error': 'Please provide a URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        metadata, error = CitationService.autocite(url)

        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'metadata': metadata})


class CitationListAPI(APIView):
    """GET/POST/DELETE for managing citation lists."""

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required to manage citation lists.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        lists = CitationList.objects.filter(user=request.user)
        result = []
        for cl in lists:
            citations = cl.citations.all()
            result.append({
                'id': cl.id,
                'name': cl.name,
                'style': cl.style.code if cl.style else 'apa',
                'citations': [
                    {
                        'id': c.id,
                        'source_type': c.source_type,
                        'metadata': c.metadata,
                        'formatted_text': c.formatted_text,
                        'in_text_citation': c.in_text_citation,
                    }
                    for c in citations
                ],
                'created_at': cl.created_at.isoformat(),
                'updated_at': cl.updated_at.isoformat(),
            })

        return Response({'lists': result})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required to manage citation lists.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = request.data
        name = data.get('name', 'My Citations')
        style_code = data.get('style', 'apa')

        style = None
        try:
            style = CitationStyle.objects.get(code=style_code)
        except CitationStyle.DoesNotExist:
            pass

        citation_list = CitationList.objects.create(
            user=request.user,
            name=name,
            style=style,
        )

        return Response({
            'id': citation_list.id,
            'name': citation_list.name,
            'style': style_code,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required to manage citation lists.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        list_id = request.query_params.get('id')
        citation_id = request.query_params.get('citation_id')

        if citation_id:
            try:
                citation = Citation.objects.get(
                    id=citation_id,
                    citation_list__user=request.user
                )
                citation.delete()
                return Response({'status': True})
            except Citation.DoesNotExist:
                return Response(
                    {'error': 'Citation not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        if list_id:
            try:
                citation_list = CitationList.objects.get(id=list_id, user=request.user)
                citation_list.delete()
                return Response({'status': True})
            except CitationList.DoesNotExist:
                return Response(
                    {'error': 'Citation list not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {'error': 'Provide list id or citation_id to delete.'},
            status=status.HTTP_400_BAD_REQUEST
        )
