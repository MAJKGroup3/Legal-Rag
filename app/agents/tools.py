# app/agents/tools.py
from __future__ import annotations

from typing import Any, Dict, Optional
import requests

from langchain_core.tools import tool

from app.services.rag_system import RAGSystem


_rag = RAGSystem()


@tool("rag_query")
def rag_query(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search the internal LegalRAG corpus (EULA/ToS/policies) and return an answer plus retrieved chunks.
    Use this for questions that should be grounded in the document set.
    """
    return _rag.query(query=query, top_k=top_k)


@tool("get_weather")
def get_weather(location: str) -> Dict[str, Any]:
    """
    Get current weather for a location using wttr.in (no API key).
    Returns basic current conditions only.
    """
    url = f"https://wttr.in/{location}?format=j1"

    try:
        data = requests.get(url, timeout=5).json()
        current = data["current_condition"][0]

        return {
            "location": location,
            "temperature_f": current.get("temp_F"),
            "condition": (current.get("weatherDesc") or [{}])[0].get("value"),
            "wind_mph": current.get("windspeedMiles"),
            "humidity_pct": current.get("humidity"),
        }

    except Exception as e:
        return {
            "location": location,
            "error": f"Weather lookup failed: {type(e).__name__}: {e}",
        }