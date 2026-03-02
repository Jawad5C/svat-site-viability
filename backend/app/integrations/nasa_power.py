"""
NASA POWER API integration for solar (and optionally wind) at a site.
Uses daily ALLSKY_SFC_SW_DWN (all-sky surface shortwave downward irradiance, kWh/m²/day).
No API key required; public API.
"""

from typing import Any, Dict, Optional

import httpx

_BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"
# One full year of daily data (e.g. last complete year)
_START = "20230101"
_END = "20231231"
_PARAMS = "ALLSKY_SFC_SW_DWN"  # Solar: kWh/m²/day
_TIMEOUT = 30.0


def get_solar_irradiance(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Fetch average daily solar irradiance (kWh/m²/day) for the given coordinates.
    Returns None on any error (network, API failure, or missing data).
    """
    url = (
        f"{_BASE}?parameters={_PARAMS}&community=RE"
        f"&longitude={longitude}&latitude={latitude}"
        f"&start={_START}&end={_END}&format=JSON"
    )
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            resp = client.get(url)
            resp.raise_for_status()
    except Exception:
        return None

    data = resp.json()
    try:
        values = data["properties"]["parameter"][_PARAMS]
        # values is dict like {"20230101": 1.78, "20230102": 1.60, ...}
        if not values:
            return None
        nums = [float(v) for v in values.values()]
        avg = sum(nums) / len(nums)
        return {"avg_daily_solar_kwh_m2": round(avg, 2), "unit": "kWh/m²/day"}
    except (KeyError, TypeError, ValueError):
        return None
