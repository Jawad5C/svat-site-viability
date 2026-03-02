"""
Simplified LCOH (Levelized Cost of Hydrogen) for a site.
Uses solar capacity factor derived from NASA POWER GHI and typical electrolyzer assumptions.
Output: $/kg H2. For MVP we use fixed assumptions; these can become configurable later.
"""

from typing import Optional

# Typical assumptions (can be made configurable or per-region later)
_CAPACITY_KW = 100_000  # 100 MW
_CAPEX_PER_KW = 1_000  # $/kW electrolyzer + balance of plant
_SPECIFIC_ENERGY_KWH_PER_KG = 50  # kWh per kg H2
_FIXED_CHARGE_RATE = 0.08  # 8% capital recovery
_OPEX_FRACTION_OF_CAPEX = 0.02  # 2% of CAPEX per year
# Solar to capacity factor: GHI daily (kWh/m²/day) -> CF. PV typically ~20% PR; CF = GHI_daily * 365 * 0.2 / 8760
_GHI_TO_CF = 365 * 0.2 / 8760  # ~0.00833


def compute_lcoh_usd_per_kg(avg_daily_solar_kwh_m2: float) -> Optional[float]:
    """
    Compute LCOH in USD per kg H2 using site solar (GHI) and fixed assumptions.
    Returns None if inputs are invalid.
    """
    if avg_daily_solar_kwh_m2 <= 0:
        return None
    capacity_factor = avg_daily_solar_kwh_m2 * _GHI_TO_CF
    # Clamp CF to a reasonable max (e.g. 35%) for very sunny sites
    capacity_factor = min(capacity_factor, 0.35)
    capex = _CAPACITY_KW * _CAPEX_PER_KW
    opex_annual = capex * _OPEX_FRACTION_OF_CAPEX
    # H2 output: kg/year = (kW * CF * 8760 h) / (kWh/kg)
    h2_kg_annual = (_CAPACITY_KW * capacity_factor * 8760) / _SPECIFIC_ENERGY_KWH_PER_KG
    if h2_kg_annual <= 0:
        return None
    lcoh = (capex * _FIXED_CHARGE_RATE + opex_annual) / h2_kg_annual
    return round(lcoh, 2)
