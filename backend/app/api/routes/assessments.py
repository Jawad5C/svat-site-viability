from fastapi import APIRouter, HTTPException

from app.models.schemas import AssessmentRequest, AssessmentResponse
from app.services.assessment_service import run_assessment
from app.utils.geo import is_in_us

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("", response_model=AssessmentResponse)
def create_assessment(body: AssessmentRequest) -> AssessmentResponse:
    """Run a site viability assessment for the given location and assessment type. MVP: US only."""
    if not is_in_us(body.location.latitude, body.location.longitude):
        raise HTTPException(
            status_code=400,
            detail="MVP supports US locations only. International support coming later.",
        )
    return run_assessment(body.assessment_type, body.location)
