"""
Point d'entrée de l'API (FastAPI) — montera les routes / orchestrera l’agent.
"""
# src/main.py
from fastapi import FastAPI
from src.front.api import router as api_router

app = FastAPI(title="Agentic Research Assistant", version="0.1.0")
app.include_router(api_router, prefix="/api")
