"""
Ranking & Qualité :
- Score = f(pertinence sémantique, fraîcheur, qualité source, signaux sociaux)
- Anti-doublons, clustering thématique (HDBSCAN)
"""
# src/core/ranking.py
from __future__ import annotations
from datetime import datetime, timezone


def _recency_score(iso_date: str | None, days_half_life: float = 14.0) -> float:
    if not iso_date:
        return 0.0
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    except Exception:
        return 0.0
    age_days = (datetime.now(timezone.utc) - dt).days + 0.0001
    # décroissance exponentielle (poids plus fort si récent)
    return 0.5 ** (age_days / days_half_life)


def score_item(item: dict, topic: str) -> float:
    title = (item.get("title") or "").lower()
    topic_l = topic.lower()
    # pertinence très simple: présence de mots du topic dans le titre
    term_hits = sum(1 for w in topic_l.split() if w in title)
    rel = 0.2 + 0.2 * min(term_hits, 3)  # 0.2 à 0.8
    # fraîcheur (news) ou année (papers)
    if item.get("type") == "news":
        rec = _recency_score(item.get("date"))
    else:
        year = item.get("year") or 0
        rec = 1.0 if year >= 2024 else 0.5 if year >= 2022 else 0.2
    # crédibilité source (ultra basique)
    src = (item.get("source") or "").lower()
    cred = 0.9 if any(k in src for k in [
                      "nature", "science", "arxiv", "mit", "wired", "verge", "venturebeat"]) else 0.6
    # score final (pondérations simples)
    return 0.5*rel + 0.3*rec + 0.2*cred


def rank_and_trim(items: list[dict], topic: str, k: int) -> list[dict]:
    return sorted(items, key=lambda x: score_item(x, topic), reverse=True)[:k]
