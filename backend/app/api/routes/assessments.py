from fastapi import APIRouter

from app.models.schemas import AssessmentRequest, AssessmentResponse
from app.services.assessment_service import run_assessment

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("", response_model=AssessmentResponse)
def create_assessment(body: AssessmentRequest) -> AssessmentResponse:
    """Run a site viability assessment for the given location and assessment type."""
    return run_assessment(body.assessment_type, body.location)
