"""
Collector News :
- Interroge NewsAPI / flux RSS whitelisés
- Filtre par date, déduplique (hash titre+url+date)
- Enrichit par score source/biais
"""
# src/agents/collector_news.py

# src/agents/collector_news.py
from __future__ import annotations
import feedparser
from datetime import datetime, timezone, timedelta
from dateutil import parser as dtparser

# Quelques flux tech/IA génériques (tu pourras en ajouter/supprimer)
DEFAULT_FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.technologyreview.com/feed/",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.wired.com/feed/rss",
]


def _parse_date(entry):
    # Essaie published, updated… sinon None
    for key in ("published", "updated", "created"):
        val = entry.get(key)
        if val:
            try:
                return dtparser.parse(val)
            except Exception:
                pass
    # Certains flux donnent 'published_parsed' (struct_time)
    if entry.get("published_parsed"):
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return None


def collect_news(topic: str, feeds: list[str] | None = None, max_results: int = 12, days_back: int = 30):
    """
    Parcourt des flux RSS, filtre par topic (dans titre/summary),
    et par récence. Retourne une liste de dicts normalisés.
    """
    feeds = feeds or DEFAULT_FEEDS
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    topic_l = topic.lower()

    results = []
    seen = set()  # pour dédup (titre+link)

    for url in feeds:
        try:
            d = feedparser.parse(url)
        except Exception:
            continue

        for e in d.entries:
            title = (e.get("title") or "").strip()
            summary = (e.get("summary") or e.get("description") or "").strip()
            link = (e.get("link") or "").strip()

            # petit filtre de pertinence par mot-clé
            haystack = f"{title} {summary}".lower()
            if topic_l.split()[0] not in haystack and topic_l not in haystack:
                continue

            # date et récence
            dt = _parse_date(e)
            if dt and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt and dt < cutoff:
                continue

            key = (title, link)
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "type": "news",
                "title": title,
                "date": (dt.isoformat() if dt else None),
                "source": d.feed.get("title", "RSS"),
                "url": link,
                "summary": summary,
            })
            if len(results) >= max_results:
                break

        if len(results) >= max_results:
            break

    return results
