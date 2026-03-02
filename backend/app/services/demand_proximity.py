"""
Demand proximity: curated summary and score by state (offtake / buyers nearby).
Data in backend/data/demand_proximity_by_state.json.
demand_score 1–5: higher = stronger potential offtake / buyer cluster for H2.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "demand_proximity_by_state.json"

_loaded: Optional[Dict[str, Any]] = None


def _load_data() -> Dict[str, Any]:
    global _loaded
    if _loaded is not None:
        return _loaded
    if not _DATA_PATH.exists():
        _loaded = {}
        return _loaded
    try:
        with open(_DATA_PATH, encoding="utf-8") as f:
            _loaded = json.load(f)
    except Exception:
        _loaded = {}
    return _loaded


def get_demand_proximity(state_abbr: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Return demand proximity info for the state: summary, demand_score (1–5, higher = better).
    Uses "default" when state is None or not in the map.
    """
    data = _load_data()
    if not data:
        return None
    key = (state_abbr or "default").upper()
    out = data.get(key) or data.get("default")
    if not out or not isinstance(out, dict):
        return None
    return {
        "summary": out.get("summary", ""),
        "demand_score": out.get("demand_score"),
    }
