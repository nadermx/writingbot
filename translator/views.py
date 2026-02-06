import json
import logging

from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.views import GlobalVars
from translator.models import TranslationHistory
from translator.services import TranslationService, LANGUAGES
import config

logger = logging.getLogger('app')

# Build reverse lookup: lowercase language name -> language code
NAME_TO_CODE = {name.lower(): code for code, name in LANGUAGES.items()}

def get_all_language_links():
    """Return sorted list of language links for the main translator page."""
    return [
        {'name': name, 'url': f'/translate/{name.lower()}/'}
        for _, name in sorted(LANGUAGES.items(), key=lambda x: x[1])
    ]


def get_language_pairs(lang_name):
    """Build all translation pairs for a specific language."""
    sorted_langs = sorted(LANGUAGES.items(), key=lambda x: x[1])
    lang_lower = lang_name.lower()
    pairs = []
    for other_code, other_name in sorted_langs:
        if other_name.lower() == lang_lower:
            continue
        pairs.append({
            'target_name': other_name,
            'url': f'/translate/{lang_lower}-to-{other_name.lower()}/',
        })
    return pairs


class TranslatorPage(View):
    def get(self, request):
        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        languages = TranslationService.get_languages()

        return render(
            request,
            'tools/translator.html',
            {
                'title': f"Translator | {config.PROJECT_NAME}",
                'description': 'Translate text between 60+ languages instantly. Free online translator powered by AI.',
                'page': 'translator',
                'g': settings,
                'is_premium': is_premium,
                'languages_json': json.dumps(languages),
                'language_links': get_all_language_links(),
            }
        )


class TranslationLanguagePage(View):
    """
    SEO landing page for a specific language, e.g. /translate/english/
    Shows an embedded translator pre-set to that language + all translation pairs.
    """

    def get(self, request, language):
        lang_lower = language.lower()
        lang_code = NAME_TO_CODE.get(lang_lower)
        if not lang_code:
            raise Http404

        lang_name = LANGUAGES[lang_code]
        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        languages_list = TranslationService.get_languages()
        pairs = get_language_pairs(lang_name)

        # Pick a sensible default target (English if source isn't English, else Spanish)
        if lang_code == 'en':
            default_target = 'es'
        else:
            default_target = 'en'

        seo = {
            'h1': f'{lang_name} Translator',
            'subtitle': f'Translate {lang_name} to and from {len(pairs)} languages with AI',
            'meta_title': f'{lang_name} Translator - Translate {lang_name} Online Free | {config.PROJECT_NAME}',
            'meta_description': (
                f'Free online {lang_name} translator. Translate {lang_name} to and from '
                f'{len(pairs)} languages instantly with AI-powered accuracy.'
            ),
            'features': [
                {
                    'title': f'Accurate {lang_name} Translation',
                    'text': (
                        f'Our AI translator understands the nuances of {lang_name}, '
                        f'delivering accurate translations that preserve meaning and context.'
                    ),
                },
                {
                    'title': 'Instant Results',
                    'text': (
                        f'Translate {lang_name} text in seconds. '
                        f'No waiting, no sign-up required. Just paste your text and get results.'
                    ),
                },
                {
                    'title': 'Natural-Sounding Output',
                    'text': (
                        f'Get translations that read naturally, not like machine output. '
                        f'Our AI produces fluent, human-quality translations every time.'
                    ),
                },
            ],
            'faqs': [
                {
                    'q': f'How many languages can I translate {lang_name} to?',
                    'a': (
                        f'You can translate {lang_name} to and from {len(pairs)} languages '
                        f'including English, Spanish, French, German, Chinese, Japanese, '
                        f'Arabic, Hindi, and many more.'
                    ),
                },
                {
                    'q': f'Is the {lang_name} translator free?',
                    'a': (
                        f'Yes, you can translate up to 5,000 characters of {lang_name} text '
                        f'completely free. Premium users get unlimited translations with priority processing.'
                    ),
                },
                {
                    'q': f'How accurate is the {lang_name} translator?',
                    'a': (
                        f'Our AI-powered {lang_name} translator delivers high-accuracy translations '
                        f'by understanding context, grammar, and idiomatic expressions. '
                        f'It handles everyday conversation, business documents, and academic text.'
                    ),
                },
                {
                    'q': f'Can I translate documents from {lang_name}?',
                    'a': (
                        f'You can paste text directly from any document to translate it from {lang_name}. '
                        f'Simply copy your text, paste it into the translator, select your target language, '
                        f'and click Translate.'
                    ),
                },
            ],
        }

        return render(
            request,
            'translator/language.html',
            {
                'title': seo['meta_title'],
                'description': seo['meta_description'],
                'page': 'translator',
                'g': settings,
                'seo': seo,
                'is_premium': is_premium,
                'languages_json': json.dumps(languages_list),
                'default_source': lang_code,
                'default_target': default_target,
                'lang_name': lang_name,
                'pairs': pairs,
                'language_links': get_all_language_links(),
            }
        )


class TranslateAPI(APIView):
    def post(self, request):
        data = request.data
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', '')

        if not text:
            return Response(
                {'error': 'Please provide text to translate.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not target_lang:
            return Response(
                {'error': 'Please select a target language.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        char_count = len(text)

        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )

        # Character limit for free users
        if not is_premium and char_count > 5000:
            return Response(
                {
                    'error': 'Free users are limited to 5,000 characters. Upgrade to Premium for unlimited translations.',
                    'limit_exceeded': True,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Run translation
        result, error = TranslationService.translate(text, source_lang, target_lang)

        if error:
            return Response(
                {'error': error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save history
        try:
            TranslationHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                input_text=text,
                output_text=result['translated_text'],
                source_lang=result['source_lang'],
                target_lang=result['target_lang'],
                char_count=char_count,
            )
        except Exception as e:
            logger.error(f'Failed to save translation history: {str(e)}')

        return Response({
            'translated_text': result['translated_text'],
            'source_lang': result['source_lang'],
            'target_lang': result['target_lang'],
            'char_count': char_count,
        })


class LanguagesAPI(APIView):
    def get(self, request):
        languages = TranslationService.get_languages()
        return Response({'languages': languages})


class TranslationPairPage(View):
    """
    SEO landing page for a specific translation pair, e.g. /translate/english-to-spanish/
    Dynamically generates content based on the source and target language names.
    """

    def get(self, request, source, target):
        # Validate languages
        source_lower = source.lower()
        target_lower = target.lower()

        source_code = NAME_TO_CODE.get(source_lower)
        target_code = NAME_TO_CODE.get(target_lower)

        if not source_code or not target_code:
            raise Http404

        if source_code == target_code:
            raise Http404

        # Proper-cased names
        source_name = LANGUAGES[source_code]
        target_name = LANGUAGES[target_code]

        settings = GlobalVars.get_globals(request)
        is_premium = (
            request.user.is_authenticated and request.user.is_plan_active
        )
        languages = TranslationService.get_languages()

        # Build SEO content
        seo = {
            'h1': f'Translate {source_name} to {target_name} Online Free',
            'subtitle': (
                f'Free {source_name} to {target_name} translator powered by AI. '
                f'Translate text, sentences, and paragraphs instantly.'
            ),
            'meta_title': f'{source_name} to {target_name} Translation | {config.PROJECT_NAME}',
            'meta_description': (
                f'Free online {source_name} to {target_name} translator. '
                f'Translate text instantly with AI-powered accuracy. No sign-up required.'
            ),
            'features': [
                {
                    'title': f'Accurate {source_name} to {target_name}',
                    'text': (
                        f'Our AI translator understands the nuances of both {source_name} and {target_name}, '
                        f'delivering accurate translations that preserve meaning and context.'
                    ),
                },
                {
                    'title': 'Instant Translation',
                    'text': (
                        f'Translate {source_name} text to {target_name} in seconds. '
                        f'No waiting, no sign-up required. Just paste your text and get results.'
                    ),
                },
                {
                    'title': 'Natural-Sounding Output',
                    'text': (
                        f'Get {target_name} translations that read naturally, not like machine output. '
                        f'Our AI produces fluent, human-quality translations every time.'
                    ),
                },
            ],
            'faqs': [
                {
                    'q': f'How accurate is this {source_name} to {target_name} translator?',
                    'a': (
                        f'Our AI-powered translator delivers high-accuracy {source_name} to {target_name} '
                        f'translations by understanding context, grammar, and idiomatic expressions in both '
                        f'languages. It handles everyday conversation, business documents, and academic text.'
                    ),
                },
                {
                    'q': f'Is the {source_name} to {target_name} translator free?',
                    'a': (
                        f'Yes, you can translate up to 5,000 characters from {source_name} to {target_name} '
                        f'completely free. Premium users get unlimited translations with priority processing.'
                    ),
                },
                {
                    'q': f'Can I translate {target_name} back to {source_name}?',
                    'a': (
                        f'Absolutely! You can use the swap button to quickly switch the translation direction '
                        f'from {target_name} to {source_name}, or visit our '
                        f'<a href="/translate/{target_lower}-to-{source_lower}/">'
                        f'{target_name} to {source_name} translator</a>.'
                    ),
                },
                {
                    'q': f'What types of text can I translate from {source_name} to {target_name}?',
                    'a': (
                        f'You can translate any type of text including emails, documents, articles, '
                        f'essays, social media posts, and more from {source_name} to {target_name}. '
                        f'The translator handles both formal and informal language.'
                    ),
                },
            ],
        }

        # Build pairs for source language (other translations from this language)
        source_pairs = get_language_pairs(source_name)

        return render(
            request,
            'translator/pair.html',
            {
                'title': seo['meta_title'],
                'description': seo['meta_description'],
                'page': 'translator',
                'g': settings,
                'seo': seo,
                'is_premium': is_premium,
                'languages_json': json.dumps(languages),
                'default_source': source_code,
                'default_target': target_code,
                'source_name': source_name,
                'target_name': target_name,
                'source_pairs': source_pairs,
            }
        )
