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
