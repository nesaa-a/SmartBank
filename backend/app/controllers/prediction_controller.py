from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction import LoanPredictionRequest, LoanPredictionResponse
from app.services import prediction_service

router = APIRouter(prefix="/loan", tags=["loan-prediction"])


@router.post(
    "/predict",
    response_model=LoanPredictionResponse,
    summary="Predict loan approval and maximum eligible amount",
)
async def predict_loan(payload: LoanPredictionRequest) -> LoanPredictionResponse:
    """
    Runs the trained XGBoost model on the submitted loan application data and returns:
    - **loan_approved**: whether the application is likely to be approved
    - **approval_probability**: model confidence score (0 – 1)
    - **max_loan_amount**: recommended maximum loan the applicant qualifies for
    - **risk_level**: Low | Medium | High
    - **factors**: key reasons behind the decision
    """
    try:
        return prediction_service.predict(payload)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
