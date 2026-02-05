import logging
import re
from datetime import datetime
from difflib import SequenceMatcher
from urllib.parse import quote_plus

import requests
from django.conf import settings
from django.utils import timezone

from plagiarism.models import PlagiarismReport, PlagiarismUsage

logger = logging.getLogger('app')

MONTHLY_WORD_LIMIT = settings.TOOL_LIMITS.get('plagiarism', {}).get('premium_monthly_words', 30000)


class PlagiarismService:

    @staticmethod
    def check_monthly_usage(user):
        """
        Returns dict with words used this month vs the monthly limit.
        """
        now = timezone.now()
        month_start = now.replace(day=1).date()

        usage, _ = PlagiarismUsage.objects.get_or_create(
            user=user,
            month=month_start,
            defaults={'words_used': 0}
        )

        return {
            'words_used': usage.words_used,
            'words_limit': MONTHLY_WORD_LIMIT,
            'words_remaining': max(0, MONTHLY_WORD_LIMIT - usage.words_used),
            'month': month_start.strftime('%B %Y'),
        }

    @staticmethod
    def check_plagiarism(text, user):
        """
        Premium only. Check text for plagiarism by searching the web for matching content.
        Returns (result_dict, error_string).
        """
        if not text or not text.strip():
            return None, 'Please provide text to check.'

        word_count = len(text.split())
        if word_count < 15:
            return None, 'Please provide at least 15 words to check for plagiarism.'

        # Check monthly usage
        usage_info = PlagiarismService.check_monthly_usage(user)
        if usage_info['words_remaining'] < word_count:
            return None, (
                f'Monthly word limit exceeded. You have {usage_info["words_remaining"]} words remaining '
                f'out of {MONTHLY_WORD_LIMIT:,} this month.'
            )

        try:
            # Break text into segments for searching
            segments = PlagiarismService._split_into_segments(text)
            all_matches = []
            seen_urls = set()

            for segment in segments:
                segment_matches = PlagiarismService._search_segment(segment)
                for match in segment_matches:
                    if match['source_url'] not in seen_urls:
                        seen_urls.add(match['source_url'])
                        all_matches.append(match)

            # Calculate overall similarity
            if all_matches:
                total_similarity = sum(m['similarity_percent'] for m in all_matches)
                similarity_percentage = min(round(total_similarity / len(all_matches), 1), 100.0)
            else:
                similarity_percentage = 0.0

            # Sort matches by similarity (highest first)
            all_matches.sort(key=lambda m: m['similarity_percent'], reverse=True)

            # Cap at top 20 matches
            all_matches = all_matches[:20]

            # Update monthly usage
            now = timezone.now()
            month_start = now.replace(day=1).date()
            usage, _ = PlagiarismUsage.objects.get_or_create(
                user=user,
                month=month_start,
                defaults={'words_used': 0}
            )
            usage.words_used += word_count
            usage.save()

            # Save report
            report = PlagiarismReport.objects.create(
                user=user,
                input_text=text,
                similarity_percentage=similarity_percentage,
                word_count=word_count,
                matches=all_matches,
                words_used_this_month=usage.words_used,
            )

            return {
                'report_id': report.id,
                'similarity_percentage': similarity_percentage,
                'word_count': word_count,
                'matches': all_matches,
                'usage': {
                    'words_used': usage.words_used,
                    'words_limit': MONTHLY_WORD_LIMIT,
                    'words_remaining': max(0, MONTHLY_WORD_LIMIT - usage.words_used),
                },
            }, None

        except Exception as e:
            logger.error(f'Plagiarism check error: {e}')
            return None, f'An error occurred while checking for plagiarism. Please try again.'

    @staticmethod
    def _split_into_segments(text, segment_size=30):
        """Split text into overlapping segments of roughly segment_size words."""
        words = text.split()
        segments = []
        step = max(segment_size // 2, 10)

        for i in range(0, len(words), step):
            segment = ' '.join(words[i:i + segment_size])
            if len(segment.split()) >= 8:
                segments.append(segment)

        # Limit number of segments to avoid excessive requests
        if len(segments) > 10:
            # Take evenly spaced segments
            step = len(segments) // 10
            segments = [segments[i] for i in range(0, len(segments), step)][:10]

        return segments

    @staticmethod
    def _search_segment(segment):
        """
        Search the web for a text segment and compare results.
        Returns list of match dicts.
        """
        matches = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; WritingBot/1.0; +https://writingbot.ai)'
        }

        # Use a quoted search to find exact or near-exact matches
        # Extract a key phrase (first ~10 words) for searching
        words = segment.split()
        search_phrase = ' '.join(words[:12])
        query = quote_plus(f'"{search_phrase}"')

        try:
            # Search using a simple web search approach
            search_url = f'https://html.duckduckgo.com/html/?q={query}'
            response = requests.get(search_url, headers=headers, timeout=8)

            if response.status_code != 200:
                return matches

            html = response.text

            # Extract result links and snippets
            results = re.findall(
                r'<a[^>]+class="result__a"[^>]+href="([^"]*)"[^>]*>([^<]*)</a>.*?'
                r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
                html,
                re.DOTALL
            )

            for result_url, result_title, snippet in results[:5]:
                # Clean HTML from snippet
                clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                clean_title = re.sub(r'<[^>]+>', '', result_title).strip()

                if not clean_snippet or not result_url:
                    continue

                # Calculate similarity between segment and snippet
                similarity = SequenceMatcher(
                    None,
                    segment.lower(),
                    clean_snippet.lower()
                ).ratio() * 100

                if similarity >= 20:
                    matches.append({
                        'source_url': result_url,
                        'matched_text': clean_snippet[:500],
                        'similarity_percent': round(similarity, 1),
                        'title': clean_title[:200],
                    })

        except requests.exceptions.RequestException as e:
            logger.warning(f'Plagiarism search request failed: {e}')
        except Exception as e:
            logger.error(f'Plagiarism segment search error: {e}')

        return matches
