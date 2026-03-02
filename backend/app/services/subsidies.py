"""
Policy & subsidy matcher: returns US hydrogen-related programs applicable to a state.
Data in backend/data/us_h2_subsidies.json; federal programs apply to all states.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "us_h2_subsidies.json"

_loaded: Optional[List[Dict[str, Any]]] = None


def _load_subsidies() -> List[Dict[str, Any]]:
    global _loaded
    if _loaded is not None:
        return _loaded
    if not _DATA_PATH.exists():
        _loaded = []
        return _loaded
    try:
        with open(_DATA_PATH, encoding="utf-8") as f:
            _loaded = json.load(f)
    except Exception:
        _loaded = []
    return _loaded


def get_subsidies_for_state(state_abbr: Optional[str]) -> List[Dict[str, Any]]:
    """
    Return list of subsidy programs applicable to the given state.
    If state_abbr is None, returns only federal (states: "all") programs.
    Each item has keys: id, name, type, summary, link.
    """
    programs = _load_subsidies()
    out = []
    for p in programs:
        states = p.get("states")
        if states == "all":
            out.append(p)
        elif state_abbr and isinstance(states, list) and state_abbr.upper() in [s.upper() for s in states]:
            out.append(p)
    return out
