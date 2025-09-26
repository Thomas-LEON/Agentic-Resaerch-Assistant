"""
Planner (agent chef) :
- Décompose le sujet en sous-thèmes
- Génère des requêtes ciblées
- Choisit les outils (ReAct/Reflexion) et priorise les sources
"""
# src/agents/planner.py


def plan(topic: str):
    """
    Découpe le sujet en sous-thèmes (naïf pour démarrer).
    Sert à construire des requêtes ciblées pour les collecteurs.
    """
    topic = topic.strip()
    return [
        topic,
        f"{topic} AND applications",
        f"{topic} AND evaluation",
        f"{topic} AND risks",
    ]
