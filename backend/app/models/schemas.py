from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AssessmentType(str, Enum):
    """Where the user is in their project. Determines which metrics we return."""

    FULL = "full"  # Haven't started — all metrics (Gaps 1 + 2 + 3)
    POST_FID = "post_fid"  # Have funding — Gap 2 only
    POST_CONSTRUCTION = "post_construction"  # Already building — Gap 3 only


class LocationInput(BaseModel):
    """Site location. MVP: US only. Lat/long used for solar/wind and regional data."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude (WGS84)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (WGS84)")


class AssessmentRequest(BaseModel):
    """Request body for running a site viability assessment."""

    assessment_type: AssessmentType = Field(
        ...,
        description="Full assessment, or only Gap 2 (post-FID) or Gap 3 (post-construction) metrics",
    )
    location: LocationInput = Field(..., description="Site coordinates (US only for MVP)")


class MetricResult(BaseModel):
    """One metric in the assessment result."""

    id: str = Field(..., description="Machine-readable metric id")
    name: str = Field(..., description="User-facing label (e.g. 'Buyers nearby?')")
    value: Optional[float] = Field(None, description="Numeric score or value when available")
    status: Optional[str] = Field(
        None,
        description="e.g. 'suggest_further_research' when we cannot compute a value",
    )
    message: Optional[str] = Field(
        None,
        description="Plain-language note, e.g. recommendation to get specialist advice",
    )


class AssessmentResponse(BaseModel):
    """Response for a site viability assessment."""

    assessment_type: AssessmentType
    location: LocationInput
    metrics: list[MetricResult] = Field(
        ...,
        description="Metrics relevant to the requested assessment type",
    )
