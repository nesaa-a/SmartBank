from pydantic import BaseModel, Field


class LoanPredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Applicant age in years")
    annual_income: float = Field(..., gt=0, description="Annual income in currency units")
    monthly_expenses: float = Field(..., ge=0, description="Monthly living expenses")
    employment_status: str = Field(
        ...,
        description="One of: employed, self_employed, unemployed, retired, part_time",
    )
    contract_type: str = Field(
        ...,
        description="One of: permanent, temporary, contract, freelance",
    )
    existing_debt: float = Field(..., ge=0, description="Total existing outstanding debt")
    requested_amount: float = Field(..., gt=0, description="Loan amount requested")
    term_months: int = Field(..., ge=6, le=360, description="Desired loan duration in months")
    credit_score: int = Field(..., ge=300, le=850, description="Credit bureau score")
    num_dependents: int = Field(..., ge=0, le=20, description="Number of financial dependents")
    has_property: bool = Field(..., description="Whether applicant owns real property")
    previous_defaults: int = Field(..., ge=0, description="Number of previous loan defaults")


class LoanPredictionResponse(BaseModel):
    loan_approved: bool
    approval_probability: float = Field(..., description="Model confidence (0.0 – 1.0)")
    max_loan_amount: float = Field(..., description="Recommended maximum loan amount")
    risk_level: str = Field(..., description="Low | Medium | High")
    model_version: str
    factors: dict = Field(..., description="Key decision factors with direction (+/-)")
