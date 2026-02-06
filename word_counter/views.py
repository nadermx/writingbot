from django.views import View
from django.shortcuts import render
from accounts.views import GlobalVars


class WordCounterPage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)

        context = {
            'g': g,
            'title': f"{g.get('i18n', {}).get('word_counter', 'Word Counter')} - {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free online word counter tool. Count words, characters, sentences, paragraphs, and get readability scores in real time.',
            'page': 'word_counter',
        }
        return render(request, 'tools/word-counter.html', context)


class CharacterCounterPage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)

        context = {
            'g': g,
            'title': f"Character Counter | {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free online character counter. Count characters in real time and check limits for Twitter/X, Facebook, Instagram, LinkedIn, SMS, SEO titles, and more.',
            'page': 'character_counter',
        }
        return render(request, 'tools/character-counter.html', context)


class TextCaseConverterPage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)

        context = {
            'g': g,
            'title': f"Text Case Converter | {g.get('project_name', 'WritingBot.ai')}",
            'description': 'Free online text case converter. Convert text to UPPERCASE, lowercase, Title Case, camelCase, snake_case, kebab-case, and more with one click.',
            'page': 'text_case_converter',
        }
        return render(request, 'tools/text-case-converter.html', context)
