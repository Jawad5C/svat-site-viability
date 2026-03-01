"""
Assessment logic: returns metrics for the requested assessment type.
MVP: stub implementation. Real data (NASA POWER, WRI Aqueduct, etc.) to be wired in later.
"""

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
    """Run a site viability assessment. Returns stub metrics for the requested type."""
    metrics: list[MetricResult] = []

    if assessment_type == AssessmentType.FULL:
        for mid, name in GAP_1_METRICS + GAP_2_METRICS + GAP_3_METRICS:
            metrics.append(_stub_metric(mid, name))
    elif assessment_type == AssessmentType.POST_FID:
        for mid, name in GAP_2_METRICS:
            metrics.append(_stub_metric(mid, name))
    else:  # POST_CONSTRUCTION
        for mid, name in GAP_3_METRICS:
            metrics.append(_stub_metric(mid, name))

    return AssessmentResponse(
        assessment_type=assessment_type,
        location=location,
        metrics=metrics,
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
