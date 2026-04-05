"""
News Headline Scraper + Gematria Pipeline

Fetches headlines from CNN and Vatican News RSS feeds,
then runs each headline through all gematria calculators
to produce numerical values for the prediction formula.

Client theory: CNN/Vatican headlines contain numerological signals
that can be decoded via gematria to improve prediction accuracy.
"""
import logging
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path(__file__).parent.parent.parent / 'data' / 'news_cache'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/xml, application/rss+xml, text/xml, text/html',
}

# RSS feed URLs
RSS_FEEDS = {
    'CNN': [
        'http://rss.cnn.com/rss/cnn_topstories.rss',
        'http://rss.cnn.com/rss/cnn_latest.rss',
    ],
    'VATICAN': [
        'https://www.vaticannews.va/en.rss.xml',
    ],
}


class NewsScraper:
    """Fetches news headlines and runs them through gematria calculators."""

    def __init__(self, cache_minutes: int = 30):
        self.cache_minutes = cache_minutes
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        os.makedirs(CACHE_DIR, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        return CACHE_DIR / f"{key}.json"

    def _get_cached(self, key: str) -> Optional[dict]:
        path = self._get_cache_path(key)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cached_time = datetime.fromisoformat(data['_cached_at'])
                if datetime.now() - cached_time < timedelta(minutes=self.cache_minutes):
                    return data.get('_payload')
            except Exception:
                pass
        return None

    def _save_cache(self, key: str, payload):
        path = self._get_cache_path(key)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'_cached_at': datetime.now().isoformat(), '_payload': payload}, f)
        except Exception as e:
            logger.debug(f"Cache write error: {e}")

    def _parse_rss(self, xml_text: str) -> List[Dict]:
        """Parse RSS XML and extract headlines."""
        headlines = []
        try:
            root = ET.fromstring(xml_text)
            # Handle both RSS 2.0 and Atom feeds
            items = root.findall('.//item')
            if not items:
                # Try Atom format
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                items = root.findall('.//atom:entry', ns)

            for item in items:
                title = None
                pub_date = None
                description = None

                # RSS 2.0
                title_el = item.find('title')
                if title_el is not None and title_el.text:
                    title = title_el.text.strip()

                date_el = item.find('pubDate')
                if date_el is not None and date_el.text:
                    pub_date = date_el.text.strip()

                desc_el = item.find('description')
                if desc_el is not None and desc_el.text:
                    description = desc_el.text.strip()[:200]

                # Atom format fallback
                if not title:
                    title_el = item.find('{http://www.w3.org/2005/Atom}title')
                    if title_el is not None and title_el.text:
                        title = title_el.text.strip()

                if title:
                    headlines.append({
                        'title': title,
                        'date': pub_date or '',
                        'description': description or '',
                    })
        except ET.ParseError as e:
            logger.error(f"RSS parse error: {e}")

        return headlines

    def fetch_headlines(self, source: str = 'CNN', limit: int = 20) -> List[Dict]:
        """
        Fetch headlines from a news source.

        Args:
            source: 'CNN' or 'VATICAN'
            limit: Max headlines to return
        """
        cache_key = f"headlines_{source.lower()}_{datetime.now().strftime('%Y%m%d')}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached[:limit]

        feeds = RSS_FEEDS.get(source.upper(), [])
        if not feeds:
            return []

        all_headlines = []
        for feed_url in feeds:
            try:
                resp = self.session.get(feed_url, timeout=15)
                resp.raise_for_status()
                headlines = self._parse_rss(resp.text)
                all_headlines.extend(headlines)
            except Exception as e:
                logger.error(f"Error fetching {feed_url}: {e}")

        # Deduplicate by title
        seen = set()
        unique = []
        for h in all_headlines:
            if h['title'] not in seen:
                seen.add(h['title'])
                unique.append(h)

        self._save_cache(cache_key, unique)
        return unique[:limit]

    def analyze_headlines(self, source: str = 'CNN', limit: int = 10) -> Dict:
        """
        Fetch headlines and run each through all gematria calculators.

        Returns dict with headlines, their gematria values, and summary stats.
        """
        from apps.calculators.registry import CalculatorRegistry

        cache_key = f"analysis_{source.lower()}_{datetime.now().strftime('%Y%m%d_%H')}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        headlines = self.fetch_headlines(source, limit)
        if not headlines:
            return {'source': source, 'headlines': [], 'summary': {}}

        analyzed = []
        all_values = {}  # Aggregate values across all headlines

        for h in headlines:
            title = h['title']
            gematria = CalculatorRegistry.calculate_all(title)

            # Track aggregate values
            for calc_name, value in gematria.items():
                if calc_name not in all_values:
                    all_values[calc_name] = []
                all_values[calc_name].append(value)

            analyzed.append({
                'title': title,
                'date': h['date'],
                'gematria': gematria,
            })

        # Compute summary: average, min, max for each calculator
        summary = {}
        for calc_name, values in all_values.items():
            summary[calc_name] = {
                'avg': round(sum(values) / len(values), 2),
                'min': min(values),
                'max': max(values),
                'total': sum(values),
            }

        # Key numbers: the reduction/ordinal averages that feed into the formula
        key_calcs = ['ordinal', 'reduction', 'reverse_ordinal', 'reverse_reduction',
                     'chaldean', 'septenary', 'jewish']
        key_numbers = {}
        for calc in key_calcs:
            if calc in summary:
                key_numbers[calc] = summary[calc]['avg']

        result = {
            'source': source,
            'fetched_at': datetime.now().isoformat(),
            'headline_count': len(analyzed),
            'headlines': analyzed,
            'summary': summary,
            'key_numbers': key_numbers,
        }

        self._save_cache(cache_key, result)
        return result

    def get_combined_analysis(self, limit: int = 10) -> Dict:
        """Get analysis from all news sources combined."""
        results = {}
        combined_key_numbers = {}

        for source in RSS_FEEDS:
            analysis = self.analyze_headlines(source, limit)
            results[source] = analysis

            # Merge key numbers
            for calc, val in analysis.get('key_numbers', {}).items():
                if calc not in combined_key_numbers:
                    combined_key_numbers[calc] = []
                combined_key_numbers[calc].append(val)

        # Average across sources
        final_key_numbers = {
            calc: round(sum(vals) / len(vals), 2)
            for calc, vals in combined_key_numbers.items()
        }

        return {
            'sources': results,
            'combined_key_numbers': final_key_numbers,
            'fetched_at': datetime.now().isoformat(),
        }


# Global instance
news_scraper = NewsScraper()
