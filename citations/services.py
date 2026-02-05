import logging
import re
from datetime import datetime

import requests
from django.conf import settings

logger = logging.getLogger('app')


class CitationService:
    STYLES = {
        'apa': {'name': 'APA (7th edition)', 'code': 'apa'},
        'mla': {'name': 'MLA (9th edition)', 'code': 'mla'},
        'chicago': {'name': 'Chicago (17th edition)', 'code': 'chicago'},
        'harvard': {'name': 'Harvard', 'code': 'harvard'},
        'ieee': {'name': 'IEEE', 'code': 'ieee'},
        'ama': {'name': 'AMA (11th edition)', 'code': 'ama'},
        'vancouver': {'name': 'Vancouver', 'code': 'vancouver'},
        'turabian': {'name': 'Turabian (9th edition)', 'code': 'turabian'},
    }

    @staticmethod
    def get_styles():
        return [
            {'code': code, 'name': info['name']}
            for code, info in CitationService.STYLES.items()
        ]

    @staticmethod
    def generate_citation(source_type, metadata, style):
        """
        Generate a formatted citation and in-text citation from metadata.
        Returns (result_dict, error_string).
        """
        try:
            style = style.lower()
            formatters = {
                'apa': CitationService.format_apa,
                'mla': CitationService.format_mla,
                'chicago': CitationService.format_chicago,
                'harvard': CitationService.format_harvard,
                'ieee': CitationService.format_ieee,
                'ama': CitationService.format_ama,
                'vancouver': CitationService.format_vancouver,
                'turabian': CitationService.format_turabian,
            }

            formatter = formatters.get(style)
            if not formatter:
                return None, f'Unsupported citation style: {style}'

            formatted_text, in_text = formatter(metadata, source_type)

            return {
                'formatted_text': formatted_text,
                'in_text_citation': in_text,
                'style': style,
                'source_type': source_type,
            }, None

        except Exception as e:
            logger.error(f'Citation generation error: {e}')
            return None, str(e)

    @staticmethod
    def autocite(url):
        """
        Fetch a URL and extract citation metadata.
        Returns (metadata_dict, error_string).
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; WritingBot/1.0; +https://writingbot.ai)'
            }
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            html = response.text

            metadata = {
                'url': url,
                'title': '',
                'author': '',
                'date': '',
                'publisher': '',
            }

            # Extract title
            og_title = re.search(r'<meta\s+(?:property|name)=["\']og:title["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
            if not og_title:
                og_title = re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+(?:property|name)=["\']og:title["\']', html, re.IGNORECASE)
            if og_title:
                metadata['title'] = og_title.group(1).strip()
            else:
                title_tag = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
                if title_tag:
                    metadata['title'] = title_tag.group(1).strip()

            # Extract author
            author_meta = re.search(r'<meta\s+(?:name|property)=["\'](?:author|article:author|dc\.creator)["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
            if not author_meta:
                author_meta = re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+(?:name|property)=["\'](?:author|article:author|dc\.creator)["\']', html, re.IGNORECASE)
            if author_meta:
                metadata['author'] = author_meta.group(1).strip()

            # Extract date
            date_meta = re.search(r'<meta\s+(?:name|property)=["\'](?:article:published_time|date|dc\.date|datePublished|publication_date)["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
            if not date_meta:
                date_meta = re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+(?:name|property)=["\'](?:article:published_time|date|dc\.date|datePublished|publication_date)["\']', html, re.IGNORECASE)
            if not date_meta:
                date_meta = re.search(r'"datePublished"\s*:\s*"([^"]*)"', html)
            if date_meta:
                raw_date = date_meta.group(1).strip()
                # Try to parse and normalize the date
                for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d', '%B %d, %Y', '%b %d, %Y'):
                    try:
                        parsed = datetime.strptime(raw_date[:26].rstrip('Z'), fmt.replace('%z', ''))
                        metadata['date'] = parsed.strftime('%Y-%m-%d')
                        break
                    except ValueError:
                        continue
                if not metadata['date']:
                    metadata['date'] = raw_date[:10]

            # Extract publisher / site name
            site_name = re.search(r'<meta\s+(?:property|name)=["\']og:site_name["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
            if not site_name:
                site_name = re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+(?:property|name)=["\']og:site_name["\']', html, re.IGNORECASE)
            if not site_name:
                site_name = re.search(r'"publisher"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]*)"', html)
            if site_name:
                metadata['publisher'] = site_name.group(1).strip()
            else:
                # Fallback: extract domain as publisher
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                domain = domain.replace('www.', '')
                metadata['publisher'] = domain.split('.')[0].capitalize()

            return metadata, None

        except requests.exceptions.Timeout:
            return None, 'Request timed out. Please check the URL and try again.'
        except requests.exceptions.RequestException as e:
            logger.error(f'Autocite fetch error for {url}: {e}')
            return None, f'Could not fetch the URL: {str(e)}'
        except Exception as e:
            logger.error(f'Autocite error: {e}')
            return None, str(e)

    # ---------------------------------------------------------------
    # Helper: parse author name into parts
    # ---------------------------------------------------------------
    @staticmethod
    def _parse_author(author_str):
        """Parse an author string. Returns (last, first, full)."""
        if not author_str:
            return '', '', ''
        author_str = author_str.strip()
        if ',' in author_str:
            parts = [p.strip() for p in author_str.split(',', 1)]
            return parts[0], parts[1] if len(parts) > 1 else '', author_str
        parts = author_str.split()
        if len(parts) >= 2:
            return parts[-1], ' '.join(parts[:-1]), author_str
        return author_str, '', author_str

    @staticmethod
    def _format_date_part(date_str, fmt='full'):
        """Convert YYYY-MM-DD to formatted date string."""
        if not date_str:
            return 'n.d.'
        try:
            d = datetime.strptime(date_str[:10], '%Y-%m-%d')
            if fmt == 'year':
                return d.strftime('%Y')
            elif fmt == 'month_year':
                return d.strftime('%B %Y')
            elif fmt == 'mla':
                return d.strftime('%-d %b. %Y') if d.month not in (5, 6, 7) else d.strftime('%-d %B %Y')
            elif fmt == 'full':
                return d.strftime('%B %-d, %Y')
            elif fmt == 'chicago':
                return d.strftime('%B %-d, %Y')
            return d.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return date_str

    @staticmethod
    def _get_access_date():
        return datetime.now().strftime('%B %-d, %Y')

    # ---------------------------------------------------------------
    # APA (7th edition)
    # ---------------------------------------------------------------
    @staticmethod
    def format_apa(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')
        isbn = metadata.get('isbn', '')

        last, first, full = CitationService._parse_author(author)
        year = CitationService._format_date_part(date, 'year')
        author_ref = f'{last}, {first[0]}.' if last and first else (last or full or '')

        if source_type == 'website':
            ref = f'{author_ref} ({year}). {title}. ' if author_ref else f'{title}. ({year}). '
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += url
            in_text = f'({last or publisher or title[:30]}, {year})'

        elif source_type == 'book':
            ref = f'{author_ref} ({year}). '
            ref += f'<em>{title}</em>'
            if publisher:
                ref += f'. {publisher}'
            if doi:
                ref += f'. https://doi.org/{doi}'
            elif isbn:
                ref += f'. ISBN: {isbn}'
            ref += '.'
            in_text = f'({last or full or "Unknown"}, {year})'

        elif source_type == 'journal':
            ref = f'{author_ref} ({year}). {title}. '
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em>'
            if volume:
                ref += f', <em>{volume}</em>'
            if issue:
                ref += f'({issue})'
            if pages:
                ref += f', {pages}'
            ref += '.'
            if doi:
                ref += f' https://doi.org/{doi}'
            in_text = f'({last or full or "Unknown"}, {year})'

        elif source_type == 'article':
            ref = f'{author_ref} ({year}). {title}. '
            if publisher:
                ref += f'<em>{publisher}</em>. '
            if url:
                ref += url
            in_text = f'({last or publisher or title[:30]}, {year})'

        elif source_type == 'video':
            ref = f'{author_ref} ({year}). '
            ref += f'<em>{title}</em> [Video]. '
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += url
            in_text = f'({last or publisher or "Unknown"}, {year})'

        elif source_type == 'podcast':
            ref = f'{author_ref} (Host). ({year}). '
            ref += f'{title} [Audio podcast episode]. '
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += url
            in_text = f'({last or full or "Unknown"}, {year})'

        else:
            ref = f'{author_ref} ({year}). {title}.'
            in_text = f'({last or full or "Unknown"}, {year})'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # MLA (9th edition)
    # ---------------------------------------------------------------
    @staticmethod
    def format_mla(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        mla_date = CitationService._format_date_part(date, 'mla')
        author_ref = f'{last}, {first}' if last and first else (full or '')

        if source_type == 'website':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            ref += f'{mla_date}. ' if mla_date != 'n.d.' else ''
            if url:
                clean_url = re.sub(r'^https?://', '', url)
                ref += f'{clean_url}.'
            in_text = f'({last or publisher or title[:30]})'

        elif source_type == 'book':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}, '
            year = CitationService._format_date_part(date, 'year')
            ref += f'{year}.' if year != 'n.d.' else ''
            in_text = f'({last or full or "Unknown"})'
            if pages:
                in_text = f'({last or full or "Unknown"} {pages})'

        elif source_type == 'journal':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'"{title}." '
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em>'
            if volume:
                ref += f', vol. {volume}'
            if issue:
                ref += f', no. {issue}'
            year = CitationService._format_date_part(date, 'year')
            if year != 'n.d.':
                ref += f', {year}'
            if pages:
                ref += f', pp. {pages}'
            ref += '.'
            if doi:
                ref += f' https://doi.org/{doi}.'
            in_text = f'({last or full or "Unknown"})'
            if pages:
                in_text = f'({last or full or "Unknown"} {pages})'

        elif source_type == 'article':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            ref += f'{mla_date}. ' if mla_date != 'n.d.' else ''
            if url:
                clean_url = re.sub(r'^https?://', '', url)
                ref += f'{clean_url}.'
            in_text = f'({last or publisher or title[:30]})'

        elif source_type == 'video':
            ref = f'"{title}." '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            if author_ref:
                ref += f'uploaded by {full}, '
            ref += f'{mla_date}. ' if mla_date != 'n.d.' else ''
            if url:
                clean_url = re.sub(r'^https?://', '', url)
                ref += f'{clean_url}.'
            in_text = f'("{title[:30]}")'

        elif source_type == 'podcast':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            ref += f'{mla_date}.' if mla_date != 'n.d.' else ''
            in_text = f'({last or full or title[:30]})'

        else:
            ref = f'{author_ref}. "{title}."'
            in_text = f'({last or full or "Unknown"})'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # Chicago (17th edition) - Notes-Bibliography
    # ---------------------------------------------------------------
    @staticmethod
    def format_chicago(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        chicago_date = CitationService._format_date_part(date, 'chicago')
        year = CitationService._format_date_part(date, 'year')
        author_bib = f'{last}, {first}' if last and first else (full or '')

        if source_type == 'website':
            ref = f'{author_bib}. ' if author_bib else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'{publisher}. '
            if chicago_date != 'n.d.':
                ref += f'{chicago_date}. '
            if url:
                ref += url + '.'
            in_text = f'({last or publisher or title[:30]} {year})' if year != 'n.d.' else f'({last or publisher or title[:30]})'

        elif source_type == 'book':
            ref = f'{author_bib}. ' if author_bib else ''
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}, '
            ref += f'{year}.' if year != 'n.d.' else ''
            in_text = f'({last or full or "Unknown"} {year})'

        elif source_type == 'journal':
            ref = f'{author_bib}. ' if author_bib else ''
            ref += f'"{title}." '
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em> '
            if volume:
                ref += f'{volume}'
            if issue:
                ref += f', no. {issue}'
            if year != 'n.d.':
                ref += f' ({year})'
            if pages:
                ref += f': {pages}'
            ref += '.'
            if doi:
                ref += f' https://doi.org/{doi}.'
            in_text = f'({last or full or "Unknown"} {year})'

        elif source_type == 'article':
            ref = f'{author_bib}. ' if author_bib else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'{publisher}, '
            if chicago_date != 'n.d.':
                ref += f'{chicago_date}. '
            if url:
                ref += url + '.'
            in_text = f'({last or publisher or title[:30]} {year})'

        elif source_type == 'video':
            ref = ''
            if author_bib:
                ref += f'{author_bib}. '
            ref += f'"{title}." '
            if publisher:
                ref += f'{publisher}. '
            if chicago_date != 'n.d.':
                ref += f'{chicago_date}. '
            if url:
                ref += f'Video, {url}.'
            in_text = f'({last or full or publisher or "Unknown"} {year})'

        elif source_type == 'podcast':
            ref = f'{author_bib}. ' if author_bib else ''
            ref += f'"{title}." '
            if publisher:
                ref += f'In <em>{publisher}</em>. '
            ref += f'Podcast audio. '
            if chicago_date != 'n.d.':
                ref += f'{chicago_date}. '
            if url:
                ref += url + '.'
            in_text = f'({last or full or "Unknown"} {year})'

        else:
            ref = f'{author_bib}. "{title}." {year}.'
            in_text = f'({last or full or "Unknown"} {year})'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # Harvard
    # ---------------------------------------------------------------
    @staticmethod
    def format_harvard(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        year = CitationService._format_date_part(date, 'year')
        author_ref = f'{last}, {first[0]}.' if last and first else (last or full or '')
        access_date = CitationService._get_access_date()

        if source_type == 'website':
            ref = f'{author_ref} ({year}) ' if author_ref else f'({year}) '
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += f'Available at: {url} (Accessed: {access_date}).'
            in_text = f'({last or publisher or title[:30]}, {year})'

        elif source_type == 'book':
            ref = f'{author_ref} ({year}) '
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}.'
            in_text = f'({last or full or "Unknown"}, {year})'

        elif source_type == 'journal':
            ref = f'{author_ref} ({year}) '
            ref += f"'{title}', "
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em>'
            if volume:
                ref += f', {volume}'
            if issue:
                ref += f'({issue})'
            if pages:
                ref += f', pp. {pages}'
            ref += '.'
            if doi:
                ref += f' doi: {doi}.'
            in_text = f'({last or full or "Unknown"}, {year})'

        elif source_type == 'article':
            ref = f'{author_ref} ({year}) '
            ref += f"'{title}', "
            if publisher:
                ref += f'<em>{publisher}</em>. '
            if url:
                ref += f'Available at: {url} (Accessed: {access_date}).'
            in_text = f'({last or publisher or title[:30]}, {year})'

        elif source_type == 'video':
            ref = f'{author_ref} ({year}) ' if author_ref else f'({year}) '
            ref += f'<em>{title}</em> [Video]. '
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += f'Available at: {url} (Accessed: {access_date}).'
            in_text = f'({last or publisher or "Unknown"}, {year})'

        elif source_type == 'podcast':
            ref = f'{author_ref} ({year}) '
            ref += f"'{title}' [Podcast]. "
            if publisher:
                ref += f'{publisher}. '
            if url:
                ref += f'Available at: {url} (Accessed: {access_date}).'
            in_text = f'({last or full or "Unknown"}, {year})'

        else:
            ref = f'{author_ref} ({year}) {title}.'
            in_text = f'({last or full or "Unknown"}, {year})'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # IEEE
    # ---------------------------------------------------------------
    @staticmethod
    def format_ieee(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        year = CitationService._format_date_part(date, 'year')
        # IEEE uses initials first: F. Last
        author_ref = f'{first[0]}. {last}' if first and last else (full or '')
        access_date = CitationService._format_date_part(datetime.now().strftime('%Y-%m-%d'), 'full')

        if source_type == 'website':
            ref = f'{author_ref}, ' if author_ref else ''
            ref += f'"{title}," '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            if year != 'n.d.':
                ref += f'{year}. '
            if url:
                ref += f'[Online]. Available: {url}. [Accessed: {access_date}].'
            in_text = '[1]'

        elif source_type == 'book':
            ref = f'{author_ref}, '
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}, '
            ref += f'{year}.' if year != 'n.d.' else ''
            in_text = '[1]'

        elif source_type == 'journal':
            ref = f'{author_ref}, ' if author_ref else ''
            ref += f'"{title}," '
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em>'
            if volume:
                ref += f', vol. {volume}'
            if issue:
                ref += f', no. {issue}'
            if pages:
                ref += f', pp. {pages}'
            if year != 'n.d.':
                ref += f', {year}'
            ref += '.'
            if doi:
                ref += f' doi: {doi}.'
            in_text = '[1]'

        elif source_type == 'article':
            ref = f'{author_ref}, ' if author_ref else ''
            ref += f'"{title}," '
            if publisher:
                ref += f'<em>{publisher}</em>, '
            if year != 'n.d.':
                ref += f'{year}. '
            if url:
                ref += f'[Online]. Available: {url}.'
            in_text = '[1]'

        elif source_type == 'video':
            ref = f'{author_ref}, ' if author_ref else ''
            ref += f'"{title}," '
            if publisher:
                ref += f'{publisher}, '
            if year != 'n.d.':
                ref += f'{year}. '
            if url:
                ref += f'[Online Video]. Available: {url}.'
            in_text = '[1]'

        elif source_type == 'podcast':
            ref = f'{author_ref}, ' if author_ref else ''
            ref += f'"{title}," '
            if publisher:
                ref += f'{publisher}, '
            if year != 'n.d.':
                ref += f'{year}. '
            ref += '[Podcast].'
            if url:
                ref += f' Available: {url}.'
            in_text = '[1]'

        else:
            ref = f'{author_ref}, "{title}," {year}.'
            in_text = '[1]'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # AMA (11th edition)
    # ---------------------------------------------------------------
    @staticmethod
    def format_ama(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        year = CitationService._format_date_part(date, 'year')
        # AMA: Last FM (no period after initials, no comma)
        author_ref = f'{last} {first[0]}' if first and last else (full or '')
        access_date = CitationService._format_date_part(datetime.now().strftime('%Y-%m-%d'), 'full')

        if source_type == 'website':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title}. '
            if publisher:
                ref += f'{publisher}. '
            if date:
                pub_date = CitationService._format_date_part(date, 'full')
                ref += f'Published {pub_date}. '
            if url:
                ref += f'Accessed {access_date}. {url}'
            in_text = '1'

        elif source_type == 'book':
            ref = f'{author_ref}. '
            ref += f'<em>{title}</em>. '
            if publisher:
                ref += f'{publisher}; '
            ref += f'{year}.' if year != 'n.d.' else ''
            in_text = '1'

        elif source_type == 'journal':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title}. '
            journal_name = metadata.get('journal', publisher)
            ref += f'<em>{journal_name}</em>. '
            if year != 'n.d.':
                ref += f'{year}'
            if volume:
                ref += f';{volume}'
            if issue:
                ref += f'({issue})'
            if pages:
                ref += f':{pages}'
            ref += '.'
            if doi:
                ref += f' doi:{doi}'
            in_text = '1'

        elif source_type in ('article', 'video', 'podcast'):
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title}. '
            if publisher:
                ref += f'{publisher}. '
            if year != 'n.d.':
                ref += f'{year}. '
            if url:
                ref += f'Accessed {access_date}. {url}'
            in_text = '1'

        else:
            ref = f'{author_ref}. {title}. {year}.'
            in_text = '1'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # Vancouver
    # ---------------------------------------------------------------
    @staticmethod
    def format_vancouver(metadata, source_type):
        author = metadata.get('author', '')
        title = metadata.get('title', '')
        date = metadata.get('date', '')
        url = metadata.get('url', '')
        publisher = metadata.get('publisher', '')
        volume = metadata.get('volume', '')
        issue = metadata.get('issue', '')
        pages = metadata.get('pages', '')
        doi = metadata.get('doi', '')

        last, first, full = CitationService._parse_author(author)
        year = CitationService._format_date_part(date, 'year')
        # Vancouver: Last FM (similar to AMA)
        author_ref = f'{last} {first[0]}' if first and last else (full or '')
        access_date = CitationService._format_date_part(datetime.now().strftime('%Y-%m-%d'), 'full')

        if source_type == 'website':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title} [Internet]. '
            if publisher:
                ref += f'{publisher}; '
            if year != 'n.d.':
                ref += f'{year} '
            if url:
                ref += f'[cited {access_date}]. Available from: {url}'
            in_text = '(1)'

        elif source_type == 'book':
            ref = f'{author_ref}. '
            ref += f'{title}. '
            if publisher:
                ref += f'{publisher}; '
            ref += f'{year}.' if year != 'n.d.' else ''
            in_text = '(1)'

        elif source_type == 'journal':
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title}. '
            journal_name = metadata.get('journal', publisher)
            ref += f'{journal_name}. '
            if year != 'n.d.':
                ref += f'{year}'
            if volume:
                ref += f';{volume}'
            if issue:
                ref += f'({issue})'
            if pages:
                ref += f':{pages}'
            ref += '.'
            in_text = '(1)'

        elif source_type in ('article', 'video', 'podcast'):
            ref = f'{author_ref}. ' if author_ref else ''
            ref += f'{title} [Internet]. '
            if publisher:
                ref += f'{publisher}; '
            if year != 'n.d.':
                ref += f'{year} '
            if url:
                ref += f'[cited {access_date}]. Available from: {url}'
            in_text = '(1)'

        else:
            ref = f'{author_ref}. {title}. {year}.'
            in_text = '(1)'

        return ref.strip(), in_text

    # ---------------------------------------------------------------
    # Turabian (9th edition)
    # ---------------------------------------------------------------
    @staticmethod
    def format_turabian(metadata, source_type):
        """Turabian is essentially Chicago style for students. Uses same formatting."""
        return CitationService.format_chicago(metadata, source_type)
