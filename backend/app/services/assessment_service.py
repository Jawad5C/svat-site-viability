"""
Assessment logic: returns metrics for the requested assessment type.
Real data wired in where available (e.g. NASA POWER for solar); rest are stubs.
"""

from app.integrations.nasa_power import get_solar_irradiance
from app.services.lcoh import compute_lcoh_usd_per_kg
from app.services.subsidies import get_subsidies_for_state
from app.utils.geocode import get_state_abbr
from app.models.schemas import (
    AssessmentType,
    LocationInput,
    MetricResult,
    AssessmentResponse,
)

# Metric definitions by gap: (id, user-facing name)
GAP_1_METRICS = [
    ("demand_proximity", "Buyers nearby?"),
    ("grid_availability", "Can we connect to the grid?"),
    ("policy_subsidy_matcher", "What support can we get?"),
    ("lcoh_calculator", "Cost to produce here"),
]
GAP_2_METRICS = [
    ("infrastructure_proximity", "Ports, roads, pipelines"),
    ("water_stress_index", "Water available?"),
    ("solar_wind_data", "Sun and wind at this site"),
]
GAP_3_METRICS = [
    ("regional_risk_score", "Financing risk in this region"),
    ("electricity_price_stability", "Will electricity stay affordable?"),
    ("supply_chain_proximity", "Can we get what we need?"),
]


def run_assessment(assessment_type: AssessmentType, location: LocationInput) -> AssessmentResponse:
    """Run a site viability assessment. Returns real data where available, stubs otherwise."""
    metrics: list[MetricResult] = []

    if assessment_type == AssessmentType.FULL:
        for mid, name in GAP_1_METRICS + GAP_2_METRICS + GAP_3_METRICS:
            metrics.append(_metric_for(mid, name, location))
    elif assessment_type == AssessmentType.POST_FID:
        for mid, name in GAP_2_METRICS:
            metrics.append(_metric_for(mid, name, location))
    else:  # POST_CONSTRUCTION
        for mid, name in GAP_3_METRICS:
            metrics.append(_metric_for(mid, name, location))

    return AssessmentResponse(
        assessment_type=assessment_type,
        location=location,
        metrics=metrics,
    )


def _metric_for(metric_id: str, name: str, location: LocationInput) -> MetricResult:
    """Return real data where we have it; stub otherwise."""
    if metric_id == "solar_wind_data":
        return _solar_wind_metric(name, location)
    if metric_id == "lcoh_calculator":
        return _lcoh_metric(name, location)
    if metric_id == "policy_subsidy_matcher":
        return _policy_subsidy_metric(name, location)
    return _stub_metric(metric_id, name)


def _solar_wind_metric(name: str, location: LocationInput) -> MetricResult:
    """Sun and wind at this site: use NASA POWER solar irradiance when available."""
    data = get_solar_irradiance(location.latitude, location.longitude)
    if data is not None:
        avg = data["avg_daily_solar_kwh_m2"]
        return MetricResult(
            id="solar_wind_data",
            name=name,
            value=avg,
            status=None,
            message=f"Based on NASA POWER data: avg daily solar {avg} kWh/m²/day. Wind data can be added later.",
        )
    return MetricResult(
        id="solar_wind_data",
        name=name,
        value=None,
        status="suggest_further_research",
        message="We couldn't load solar data for this location. Consider specialist or local data.",
    )


def _lcoh_metric(name: str, location: LocationInput) -> MetricResult:
    """Cost to produce here: LCOH ($/kg H2) from NASA solar + simplified electrolyzer model."""
    data = get_solar_irradiance(location.latitude, location.longitude)
    if data is None:
        return MetricResult(
            id="lcoh_calculator",
            name=name,
            value=None,
            status="suggest_further_research",
            message="We need solar data for this site to estimate cost. Try again or use local data.",
        )
    avg_solar = data["avg_daily_solar_kwh_m2"]
    lcoh = compute_lcoh_usd_per_kg(avg_solar)
    if lcoh is None:
        return MetricResult(
            id="lcoh_calculator",
            name=name,
            value=None,
            status="suggest_further_research",
            message="Could not compute cost for this location.",
        )
    return MetricResult(
        id="lcoh_calculator",
        name=name,
        value=lcoh,
        status=None,
        message=f"Estimated LCOH: ${lcoh}/kg H2 (based on NASA solar and typical 100 MW electrolyzer assumptions).",
    )


def _policy_subsidy_metric(name: str, location: LocationInput) -> MetricResult:
    """What support can we get? Match location to US federal and state H2 programs."""
    state_abbr = get_state_abbr(location.latitude, location.longitude)
    programs = get_subsidies_for_state(state_abbr)
    if not programs:
        return MetricResult(
            id="policy_subsidy_matcher",
            name=name,
            value=0,
            status="stub",
            message="No programs in database for this location. Check IRA 45V and state incentives.",
        )
    names = [p.get("name", p.get("id", "")) for p in programs]
    msg = f"{len(programs)} program(s) may apply: " + "; ".join(names[:5])
    if len(names) > 5:
        msg += f" (and {len(names) - 5} more)."
    return MetricResult(
        id="policy_subsidy_matcher",
        name=name,
        value=float(len(programs)),
        status=None,
        message=msg,
    )


def _stub_metric(metric_id: str, name: str) -> MetricResult:
    """Return a placeholder metric. Replace with real computation later."""
    return MetricResult(
        id=metric_id,
        name=name,
        value=None,
        status="stub",
        message="Placeholder — real data will be wired in.",
    )
