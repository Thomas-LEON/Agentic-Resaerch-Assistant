# Agentic Research Assistant

## Description
Un assistant de recherche modulaire qui combine **agents spécialisés** (collecte, RAG, ranking, critique, génération) pour explorer des sources (news, publications, brevets, signaux tech), évaluer leur qualité et produire un **rapport structuré** (Markdown/PDF) incluant TL;DR, panorama rapide, bibliographie annotée, gaps et pistes de recherche.  

## Architecture
agentic-research-assistant/
├── src/               # Code source (FastAPI + agents)
│   ├── agents/        # Planner, collectors, critic, writer
│   ├── core/          # RAG, ranking, DB, config, logs
│   └── front/         # API FastAPI
├── notebooks/         # Expérimentations et évaluation
├── data/              # Données (raw, processed, eval)
├── reports/           # Rapports générés & dashboards
└── docs/              # Documentation (API, roadmap, schéma)

- Planner : décompose le sujet en sous-thèmes.
- Collectors : news (RSS/NewsAPI), papers (arXiv, OpenAlex), brevets, signaux GitHub.
- RAG : embeddings + mémoire longue (pgvector).
- Ranking : pertinence, fraîcheur, crédibilité, clustering.
- Writer : génère un rapport Markdown/PDF via templates.
- Critic : vérifie factualité (“no-source = no-claim”).
- Front API : endpoints /run, /report/{id}, /health.

## Installation
git clone https://github.com/USERNAME/agentic-research-assistant.git
cd agentic-research-assistant
pip install -r requirements.txt

### Optionnel (Docker)
docker-compose up --build
# Démarre Postgres + pgvector + Redis + API.

## Utilisation
Lancer l’API :
uvicorn src.main:app --reload

Tester un rapport :
curl -X POST http://localhost:8000/api/run \
     -H "Content-Type: application/json" \
     -d '{"topic":"AI for supply chain","max_news":5,"max_papers":5}'

Endpoints principaux :
- GET /api/health → statut
- POST /api/run → génère un rapport
- GET /api/report/{id} → contenu Markdown
- GET /api/report/{id}/download → téléchargement
- GET /api/reports → liste des rapports disponibles

## Exemple de sortie
Un rapport généré inclut :
- TL;DR (10–15 lignes)
- Panorama rapide (3–5 points clés)
- Publications (10–20 refs annotées)
- News (10 items notables)
- Gaps & pistes de recherche
- Bibliographie (BibTeX/CSL)

Voir reports/samples/

## Stack
- Backend : FastAPI, Python 3.11
- Orchestration : LangGraph/CrewAI (planned)
- DB : Postgres + pgvector, Redis
- IR/RAG : FAISS/pgvector, embeddings BGE/E5
- Obs : OpenTelemetry, Prometheus, Grafana

## Roadmap
- MVP : collectors + RAG + writer ✅
- V1 : ranking qualité + critic + observabilité 🔄
- V2 : UX front, packaging Docker, éval académique ⏳

## Licence
MIT.
