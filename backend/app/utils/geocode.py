"""
Resolve US state (abbreviation) from lat/lon for subsidy matching.
Uses Nominatim (OpenStreetMap) reverse geocoding. One request per lookup; use responsibly (see usage policy).
"""

from typing import Optional

import httpx

_NOMINATIM = "https://nominatim.openstreetmap.org/reverse"
_TIMEOUT = 10.0
_USER_AGENT = "SVAT-Site-Viability-Assessment/1.0 (contact@example.com)"

# Map state names as returned by Nominatim to two-letter abbreviation
_STATE_NAME_TO_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT",
    "delaware": "DE", "district of columbia": "DC", "florida": "FL",
    "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY",
    "louisiana": "LA", "maine": "ME", "maryland": "MD", "massachusetts": "MA",
    "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
    "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH",
    "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
    "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY",
}


def get_state_abbr(latitude: float, longitude: float) -> Optional[str]:
    """
    Return US state abbreviation (e.g. CA) for the given coordinates, or None if unknown/failed.
    Uses Nominatim; only call for points already validated as US.
    """
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            resp = client.get(
                _NOMINATIM,
                params={
                    "lat": latitude,
                    "lon": longitude,
                    "format": "json",
                    "addressdetails": 1,
                },
                headers={"User-Agent": _USER_AGENT},
            )
            resp.raise_for_status()
    except Exception:
        return None

    data = resp.json()
    if not isinstance(data, dict):
        return None
    address = data.get("address") or {}
    country = (address.get("country_code") or "").upper()
    if country != "US":
        return None
    state = address.get("state") or address.get("ISO3166-2-lvl4") or ""
    if not isinstance(state, str):
        return None
    state = state.strip()
    if state.upper().startswith("US-") and len(state) == 5:
        return state[-2:].upper()
    if len(state) == 2:
        return state.upper() if state.upper() in _STATE_NAME_TO_ABBR.values() else None
    return _STATE_NAME_TO_ABBR.get(state.lower())
