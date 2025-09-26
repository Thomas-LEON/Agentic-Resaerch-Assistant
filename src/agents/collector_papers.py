"""
Collector Papers :
- Interroge arXiv / OpenAlex / Semantic Scholar
- Récupère métadonnées + extraits
- Normalise + envoie à la couche RAG
"""

# src/agents/collector_papers.py
from __future__ import annotations
import arxiv
from datetime import datetime, timezone, timedelta


def collect_papers(topic: str, max_results: int = 12, days_back: int = 365):
    """
    Cherche des publications sur arXiv liées au topic.
    Retourne une liste de dicts normalisés.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    search = arxiv.Search(
        query=topic,
        max_results=max_results * 2,  # on sur-échantillonne puis on filtre par date
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    items = []
    for r in arxiv.Client().results(search):
        # Filtre temporel
        if r.published and r.published < cutoff:
            continue

        authors = ", ".join(a.name for a in r.authors) if r.authors else "N/A"
        url = r.entry_id or (r.pdf_url or "")
        items.append({
            "type": "paper",
            "title": r.title.strip(),
            "authors": authors,
            "year": (r.published.year if r.published else None),
            "published": r.published.isoformat() if r.published else None,
            "summary": (r.summary or "").strip(),
            "source": "arXiv",
            "url": url,
        })
        if len(items) >= max_results:
            break

    return items
