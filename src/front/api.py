"""
API (FastAPI) :
- Endpoints: /health, /run (POST/GET)
- Orchestration: planner -> collectors -> ranking -> writer
- Sauvegarde d'un rapport Markdown dans reports/samples/
"""
from pathlib import Path
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents.planner import plan
from src.agents.collector_news import collect_news
from src.agents.collector_papers import collect_papers
from src.agents.writer import write_report
from src.core.ranking import rank_and_trim
from fastapi import Response
from fastapi.responses import FileResponse, PlainTextResponse
from glob import glob


router = APIRouter()


class RunQuery(BaseModel):
    topic: str
    max_news: int | None = 10
    max_papers: int | None = 10
    days_back_news: int | None = 30
    days_back_papers: int | None = 365


@router.get("/health")
def health():
    return {"status": "ok"}


def _run_pipeline(
    topic: str,
    max_news: int = 10,
    max_papers: int = 10,
    days_back_news: int = 30,
    days_back_papers: int = 365,
):
    """
    Pipeline complète:
    planner -> collectors -> ranking -> writer -> save
    Retourne (report_id, out_path, md, news, papers).
    """
    if not topic.strip():
        raise HTTPException(status_code=400, detail="topic manquant")

    # Planner (peut générer plusieurs requêtes; ici, on ne s'en sert pas encore)
    _ = plan(topic)

    # Collecte réelle
    news = collect_news(topic, max_results=max_news, days_back=days_back_news)
    papers = collect_papers(topic, max_results=max_papers,
                            days_back=days_back_papers)

    # Ranking AVANT écriture du rapport
    news = rank_and_trim(news, topic, k=max_news)
    papers = rank_and_trim(papers, topic, k=max_papers)

    # Écriture du rapport (Markdown)
    md = write_report(topic, news=news, papers=papers)

    # Sauvegarde
    out_dir = Path("reports") / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_id = str(uuid.uuid4())[:8]
    out_path = out_dir / f"report_{report_id}.md"
    out_path.write_text(md, encoding="utf-8")

    return report_id, out_path, md, news, papers


@router.post("/run")
def run_research(q: RunQuery):
    report_id, out_path, md, news, papers = _run_pipeline(
        topic=q.topic.strip(),
        max_news=q.max_news or 10,
        max_papers=q.max_papers or 10,
        days_back_news=q.days_back_news or 30,
        days_back_papers=q.days_back_papers or 365,
    )
    return {
        "message": "rapport généré",
        "report_id": report_id,
        "path": str(out_path),
        "counts": {"news": len(news), "papers": len(papers)},
        "preview": md[:800],
    }


@router.get("/run")
def run_research_get(topic: str, max_news: int = 6, max_papers: int = 6):
    # GET pratique pour tester depuis le navigateur
    report_id, out_path, md, news, papers = _run_pipeline(
        topic=topic.strip(),
        max_news=max_news,
        max_papers=max_papers,
    )
    return {
        "message": "rapport généré (GET)",
        "report_id": report_id,
        "path": str(out_path),
        "counts": {"news": len(news), "papers": len(papers)},
        "preview": md[:800],
    }


@router.get("/report/{report_id}")
def get_report(report_id: str):
    """
    Retourne le contenu Markdown du rapport (text/markdown).
    """
    # on accepte "report_xxx.md" ou juste "xxx"
    candidates = [
        f"reports/samples/report_{report_id}.md",
        report_id if report_id.endswith(".md") else f"{report_id}.md",
    ]
    for p in candidates:
        try:
            content = Path(p).read_text(encoding="utf-8")
            return Response(content, media_type="text/markdown; charset=utf-8")
        except FileNotFoundError:
            continue
    raise HTTPException(status_code=404, detail="rapport introuvable")


@router.get("/report/{report_id}/download")
def download_report(report_id: str):
    """
    Télécharge le fichier Markdown du rapport.
    """
    p = Path(f"reports/samples/report_{report_id}.md")
    if not p.exists():
        raise HTTPException(status_code=404, detail="rapport introuvable")
    return FileResponse(path=str(p), media_type="text/markdown", filename=p.name)


@router.get("/reports")
def list_reports():
    """
    Liste rapide des rapports disponibles (pratique pour retrouver un ID).
    """
    files = sorted(glob("reports/samples/report_*.md"))
    items = [Path(f).name.replace("report_", "").replace(".md", "")
             for f in files]
    return {"count": len(items), "report_ids": items}
