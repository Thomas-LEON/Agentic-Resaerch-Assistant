"""
Writer :
- Génère un rapport via templates (Jinja/Markdown → PDF)
- Insère références numérotées et sections (TL;DR, panorama, refs annotées, gaps, etc.)
"""
# src/agents/writer.py
from __future__ import annotations
from datetime import datetime


def write_report(topic: str, news: list[dict], papers: list[dict]) -> str:
    """
    Assemble un rapport Markdown minimal à partir des news et des papers.
    (Pas de LLM ici pour l’instant → sections simples, clean)
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = []
    md.append(f"# Rapport de veille — {topic}")
    md.append(f"_Généré le {ts}_\n")

    # TL;DR naïf (top titres)
    md.append("## TL;DR")
    if news:
        md.append("- Côté actualités, voici quelques items récents liés au sujet.")
    if papers:
        md.append(
            "- Côté publications, des articles arXiv récents sont listés ci-dessous.")
    if not news and not papers:
        md.append("- Aucune source trouvée (ajuster les flux/paramètres).")
    md.append("")

    # Panorama rapide (simples bullets pour démarrer)
    md.append("## Panorama rapide")
    bullets = []
    if news:
        bullets.append(f"- {len(news)} actualités pertinentes (RSS).")
    if papers:
        bullets.append(f"- {len(papers)} publications arXiv récentes.")
    if not bullets:
        bullets.append("- Rien à signaler.")
    md.extend(bullets)
    md.append("")

    # Publications
    md.append("## Publications (arXiv)")
    if not papers:
        md.append("_Aucune publication trouvée._")
    else:
        for p in papers:
            y = p.get("year") or ""
            authors = p.get("authors") or "N/A"
            url = p.get("url") or ""
            md.append(f"- **{p['title']}** ({y}, {authors}) — [lien]({url})")
    md.append("")

    # News
    md.append("## News")
    if not news:
        md.append("_Aucune actualité trouvée._")
    else:
        for n in news:
            date = n.get("date") or ""
            src = n.get("source") or "RSS"
            url = n.get("url") or ""
            md.append(f"- **{n['title']}** ({date}) — *{src}* — [lien]({url})")
    md.append("")

    # Biblio (liens)
    md.append("## Bibliographie (liens)")
    for p in papers:
        md.append(f"- {p['title']} — {p.get('url', '')}")
    for n in news:
        md.append(f"- {n['title']} — {n.get('url', '')}")

    md.append("## TL;DR")
    if news:
        top_news = news[:2]
        for n in top_news:
            md.append(
                f"- Actu: {n['title']} ({(n.get('date') or '')}) — {n.get('source', '')}")
    if papers:
        top_papers = papers[:2]
        for p in top_papers:
            md.append(
                f"- Paper: {p['title']} ({p.get('year', '')}) — {p.get('authors', 'N/A')}")
    if not news and not papers:
        md.append("- Aucune source trouvée (ajuster les flux/paramètres).")
    md.append("")

    return "\n".join(md)
