"""
Sports Data Scraper

Fetches live sports data from public APIs:
- NBA.com CDN (scores, schedules, team data)
- ESPN public API (multi-sport scores and standings)

Reference sites (basketball-reference, etc.) are Cloudflare-blocked,
so we use official public CDN/API endpoints instead.
"""
import logging
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path(__file__).parent.parent.parent / 'data' / 'scraper_cache'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/html',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nba.com/',
}

# ESPN sport slugs
ESPN_SPORTS = {
    'NBA': 'basketball/nba',
    'WNBA': 'basketball/wnba',
    'NFL': 'football/nfl',
    'MLB': 'baseball/mlb',
    'NHL': 'hockey/nhl',
    'MLS': 'soccer/usa.1',
    'SOCCER': 'soccer/eng.1',
    'PREMIER_LEAGUE': 'soccer/eng.1',
    'LA_LIGA': 'soccer/esp.1',
    'SERIE_A': 'soccer/ita.1',
    'BUNDESLIGA': 'soccer/ger.1',
    'CHAMPIONS_LEAGUE': 'soccer/uefa.champions',
    'NCAA_BASKETBALL': 'basketball/mens-college-basketball',
    'NCAA_FOOTBALL': 'football/college-football',
}


class SportsScraper:
    """Fetches sports data from NBA.com CDN and ESPN public API."""

    def __init__(self, cache_minutes: int = 15):
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

    def _save_cache(self, key: str, payload: dict):
        path = self._get_cache_path(key)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({'_cached_at': datetime.now().isoformat(), '_payload': payload}, f)
        except Exception as e:
            logger.debug(f"Cache write error: {e}")

    def _fetch_json(self, url: str, cache_key: str = None) -> Optional[dict]:
        if cache_key:
            cached = self._get_cached(cache_key)
            if cached:
                return cached

        try:
            resp = self.session.get(url, timeout=12)
            resp.raise_for_status()
            data = resp.json()
            if cache_key:
                self._save_cache(cache_key, data)
            return data
        except Exception as e:
            logger.error(f"Fetch error {url}: {e}")
            return None

    # ── NBA.com CDN ──────────────────────────────────────────────

    def get_nba_scoreboard(self) -> List[Dict]:
        """Get today's NBA scoreboard from NBA.com CDN."""
        data = self._fetch_json(
            'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json',
            cache_key='nba_scoreboard'
        )
        if not data:
            return []

        games = []
        for g in data.get('scoreboard', {}).get('games', []):
            home = g.get('homeTeam', {})
            away = g.get('awayTeam', {})
            games.append({
                'team1': f"{away.get('teamCity', '')} {away.get('teamName', '')}".strip(),
                'team2': f"{home.get('teamCity', '')} {home.get('teamName', '')}".strip(),
                'score1': away.get('score', 0),
                'score2': home.get('score', 0),
                'team1_record': f"{away.get('wins', 0)}-{away.get('losses', 0)}",
                'team2_record': f"{home.get('wins', 0)}-{home.get('losses', 0)}",
                'status': g.get('gameStatusText', ''),
                'sport': 'NBA',
            })
        return games

    # ── ESPN Public API ──────────────────────────────────────────

    def _get_espn_slug(self, sport: str) -> Optional[str]:
        return ESPN_SPORTS.get(sport.upper())

    def get_scores(self, sport: str = 'NBA', date_str: Optional[str] = None) -> List[Dict]:
        """
        Get scores/schedule from ESPN for any sport.

        Args:
            sport: Sport key (NBA, NFL, MLB, NHL, SOCCER, etc.)
            date_str: YYYY-MM-DD format. None = today.
        """
        # For NBA today, prefer the CDN (more detail)
        if sport.upper() == 'NBA' and not date_str:
            nba_games = self.get_nba_scoreboard()
            if nba_games:
                return nba_games

        slug = self._get_espn_slug(sport)
        if not slug:
            return []

        url = f"https://site.api.espn.com/apis/site/v2/sports/{slug}/scoreboard"
        if date_str:
            url += f"?dates={date_str.replace('-', '')}"

        cache_key = f"espn_scores_{sport}_{date_str or 'today'}"
        data = self._fetch_json(url, cache_key=cache_key)
        if not data:
            return []

        games = []
        for event in data.get('events', []):
            try:
                comps = event.get('competitions', [{}])[0]
                competitors = comps.get('competitors', [])
                if len(competitors) < 2:
                    continue

                # ESPN lists home first, away second (or vice versa)
                home = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
                away = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])

                home_team = home.get('team', {})
                away_team = away.get('team', {})
                home_record = home.get('records', [{}])[0].get('summary', '') if home.get('records') else ''
                away_record = away.get('records', [{}])[0].get('summary', '') if away.get('records') else ''

                games.append({
                    'team1': away_team.get('displayName', away_team.get('name', 'TBD')),
                    'team2': home_team.get('displayName', home_team.get('name', 'TBD')),
                    'score1': away.get('score', '0'),
                    'score2': home.get('score', '0'),
                    'team1_record': away_record,
                    'team2_record': home_record,
                    'status': event.get('status', {}).get('type', {}).get('shortDetail', ''),
                    'sport': sport.upper(),
                })
            except Exception as e:
                logger.debug(f"Error parsing ESPN event: {e}")

        return games

    def get_standings(self, sport: str = 'NBA') -> Optional[Dict]:
        """
        Get standings from ESPN for any sport.

        Args:
            sport: Sport key
        """
        slug = self._get_espn_slug(sport)
        if not slug:
            return None

        url = f"https://site.api.espn.com/apis/v2/sports/{slug}/standings"
        cache_key = f"espn_standings_{sport}"
        data = self._fetch_json(url, cache_key=cache_key)

        if not data:
            return None

        standings = {'sport': sport.upper(), 'teams': []}

        for group in data.get('children', []):
            group_name = group.get('name', '')
            for entry in group.get('standings', {}).get('entries', []):
                team_info = entry.get('team', {})
                stats = {s.get('name', ''): s.get('displayValue', s.get('value', ''))
                         for s in entry.get('stats', [])}

                standings['teams'].append({
                    'team': team_info.get('displayName', team_info.get('name', '')),
                    'group': group_name,
                    'W': stats.get('wins', ''),
                    'L': stats.get('losses', ''),
                    'PCT': stats.get('winPercent', stats.get('winPct', '')),
                    'GB': stats.get('gamesBehind', ''),
                    'STRK': stats.get('streak', ''),
                    'logo': team_info.get('logos', [{}])[0].get('href', '') if team_info.get('logos') else '',
                })

        return standings if standings['teams'] else None

    def get_team_stats(self, sport: str, team_name: str) -> Optional[Dict]:
        """
        Search for a team and return info from ESPN.

        Args:
            sport: Sport key
            team_name: Team name to search
        """
        slug = self._get_espn_slug(sport)
        if not slug:
            return None

        # First get standings to find team
        standings = self.get_standings(sport)
        if not standings:
            return None

        # Find matching team
        team_name_lower = team_name.lower()
        matched = None
        for t in standings['teams']:
            if team_name_lower in t['team'].lower():
                matched = t
                break

        if not matched:
            return None

        # Also get recent scores to find team's recent games
        scores = self.get_scores(sport)
        team_games = []
        for g in scores:
            if team_name_lower in g['team1'].lower() or team_name_lower in g['team2'].lower():
                team_games.append(g)

        return {
            'team_name': matched['team'],
            'sport': sport.upper(),
            'source': 'ESPN',
            'data': {
                'Standings': {
                    'Wins': matched.get('W', ''),
                    'Losses': matched.get('L', ''),
                    'Win%': matched.get('PCT', ''),
                    'Games Behind': matched.get('GB', ''),
                    'Streak': matched.get('STRK', ''),
                    'Conference': matched.get('group', ''),
                },
                'Recent Games': {
                    f"Game {i+1}": f"{g['team1']} {g['score1']} vs {g['team2']} {g['score2']} ({g['status']})"
                    for i, g in enumerate(team_games[:5])
                } if team_games else {'Info': 'No games today'},
            }
        }

    def get_coaches(self, sport: str = 'NBA') -> List[Dict]:
        """
        Get coaches/managers for teams from ESPN API.

        Args:
            sport: Sport key
        """
        slug = self._get_espn_slug(sport)
        if not slug:
            return []

        cache_key = f"espn_coaches_{sport}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # Get teams list first
        url = f"https://site.api.espn.com/apis/site/v2/sports/{slug}/teams"
        data = self._fetch_json(url, cache_key=f"espn_teams_{sport}")
        if not data:
            return []

        coaches = []
        for group in data.get('sports', [{}])[0].get('leagues', [{}])[0].get('teams', []):
            team_info = group.get('team', {})
            team_name = team_info.get('displayName', team_info.get('name', ''))
            team_id = team_info.get('id', '')
            logo = ''
            if team_info.get('logos'):
                logo = team_info['logos'][0].get('href', '')

            coach_name = ''
            coach_exp = ''

            if team_id:
                # Coaches are on the roster endpoint
                roster_url = f"https://site.api.espn.com/apis/site/v2/sports/{slug}/teams/{team_id}/roster"
                roster = self._fetch_json(roster_url, cache_key=f"espn_roster_{sport}_{team_id}")
                if roster:
                    coach_list = roster.get('coach', [])
                    if coach_list:
                        head_coach = coach_list[0]
                        coach_name = f"{head_coach.get('firstName', '')} {head_coach.get('lastName', '')}".strip()
                        exp = head_coach.get('experience', '')
                        if exp:
                            coach_exp = f"{exp} yrs experience"

                    # Get team record from roster data
                    team_data = roster.get('team', {})
                    record = team_data.get('recordSummary', '')

            coaches.append({
                'team': team_name,
                'coach': coach_name,
                'record': record if record else coach_exp,
                'logo': logo,
                'sport': sport.upper(),
            })

        coaches = [c for c in coaches if c['coach']]
        self._save_cache(cache_key, coaches)
        return coaches

    def get_recent_games(self, sport: str = 'NBA', limit: int = 10) -> List[Dict]:
        """Get recent/today's games."""
        return self.get_scores(sport)[:limit]


# Global instance
sports_scraper = SportsScraper()
