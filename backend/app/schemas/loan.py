from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.loan import (
    ApprovedLoanStatus,
    DelinquencySeverity,
    LoanApplicationStatus,
    RiskLevel,
)
from app.schemas.common import AuditResponseMixin


class CustomerBase(BaseModel):
    customer_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone: str
    address: str
    national_id: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class CustomerResponse(CustomerBase, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class FinancialProfileCreate(BaseModel):
    customer_id: UUID
    annual_income: Decimal
    employment_status: str
    employer: str | None = None
    monthly_expenses: Decimal
    total_assets: Decimal
    total_liabilities: Decimal
    debt_to_income_ratio: Decimal


class FinancialProfileUpdate(BaseModel):
    annual_income: Decimal | None = None
    employment_status: str | None = None
    employer: str | None = None
    monthly_expenses: Decimal | None = None
    total_assets: Decimal | None = None
    total_liabilities: Decimal | None = None
    debt_to_income_ratio: Decimal | None = None


class FinancialProfileResponse(FinancialProfileCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class CreditScoreCreate(BaseModel):
    customer_id: UUID
    score: int = Field(ge=300, le=850)
    bureau: str
    report_date: date
    risk_grade: str
    factors: dict | None = None


class CreditScoreUpdate(BaseModel):
    score: int | None = Field(default=None, ge=300, le=850)
    bureau: str | None = None
    report_date: date | None = None
    risk_grade: str | None = None
    factors: dict | None = None


class CreditScoreResponse(CreditScoreCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class LoanProductCreate(BaseModel):
    code: str
    name: str
    interest_rate: Decimal
    term_months_min: int = Field(ge=1)
    term_months_max: int = Field(ge=1)
    min_credit_score: int = Field(ge=300, le=850)
    max_loan_amount: Decimal
    description: str | None = None


class LoanProductUpdate(BaseModel):
    name: str | None = None
    interest_rate: Decimal | None = None
    term_months_min: int | None = Field(default=None, ge=1)
    term_months_max: int | None = Field(default=None, ge=1)
    min_credit_score: int | None = Field(default=None, ge=300, le=850)
    max_loan_amount: Decimal | None = None
    description: str | None = None


class LoanProductResponse(LoanProductCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class LoanApplicationCreate(BaseModel):
    customer_id: UUID
    loan_product_id: UUID
    application_number: str
    requested_amount: Decimal
    term_months: int = Field(ge=1)
    purpose: str


class LoanApplicationUpdate(BaseModel):
    requested_amount: Decimal | None = None
    term_months: int | None = Field(default=None, ge=1)
    purpose: str | None = None
    status: LoanApplicationStatus | None = None


class LoanApplicationResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)

    customer_id: UUID
    loan_product_id: UUID
    application_number: str
    requested_amount: Decimal
    term_months: int
    purpose: str
    status: LoanApplicationStatus
    submitted_at: datetime | None


class RiskAssessmentResponse(AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    loan_application_id: UUID
    risk_level: RiskLevel
    risk_score: int
    model_version: str
    factors: dict | None
    assessed_at: datetime


class LoanApplicationWithRiskResponse(LoanApplicationResponse):
    risk_assessment: RiskAssessmentResponse | None = None


class CollateralCreate(BaseModel):
    loan_application_id: UUID
    collateral_type: str
    description: str
    estimated_value: Decimal
    valuation_date: date


class CollateralUpdate(BaseModel):
    collateral_type: str | None = None
    description: str | None = None
    estimated_value: Decimal | None = None
    valuation_date: date | None = None


class CollateralResponse(CollateralCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class GuarantorCreate(BaseModel):
    loan_application_id: UUID
    full_name: str
    relationship_type: str
    annual_income: Decimal
    contact_phone: str
    customer_id: UUID | None = None


class GuarantorUpdate(BaseModel):
    full_name: str | None = None
    relationship_type: str | None = None
    annual_income: Decimal | None = None
    contact_phone: str | None = None
    customer_id: UUID | None = None


class GuarantorResponse(GuarantorCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class ApprovedLoanCreate(BaseModel):
    loan_application_id: UUID
    approved_amount: Decimal
    interest_rate: Decimal
    term_months: int = Field(ge=1)
    disbursement_date: date | None = None
    status: ApprovedLoanStatus = ApprovedLoanStatus.ACTIVE


class ApprovedLoanUpdate(BaseModel):
    approved_amount: Decimal | None = None
    interest_rate: Decimal | None = None
    term_months: int | None = Field(default=None, ge=1)
    disbursement_date: date | None = None
    status: ApprovedLoanStatus | None = None


class ApprovedLoanResponse(ApprovedLoanCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class AmortizationScheduleCreate(BaseModel):
    approved_loan_id: UUID
    installment_number: int = Field(ge=1)
    due_date: date
    principal_amount: Decimal
    interest_amount: Decimal
    remaining_balance: Decimal
    is_paid: bool = False


class AmortizationScheduleUpdate(BaseModel):
    due_date: date | None = None
    principal_amount: Decimal | None = None
    interest_amount: Decimal | None = None
    remaining_balance: Decimal | None = None
    is_paid: bool | None = None


class AmortizationScheduleResponse(AmortizationScheduleCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class RepaymentCreate(BaseModel):
    approved_loan_id: UUID
    amount: Decimal
    payment_date: date
    payment_method: str
    reference_number: str


class RepaymentUpdate(BaseModel):
    amount: Decimal | None = None
    payment_date: date | None = None
    payment_method: str | None = None
    reference_number: str | None = None


class RepaymentResponse(RepaymentCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class DelinquencyCreate(BaseModel):
    approved_loan_id: UUID
    days_overdue: int = Field(ge=0)
    overdue_amount: Decimal
    severity: DelinquencySeverity
    notes: str | None = None


class DelinquencyUpdate(BaseModel):
    days_overdue: int | None = Field(default=None, ge=0)
    overdue_amount: Decimal | None = None
    severity: DelinquencySeverity | None = None
    resolved_at: datetime | None = None
    notes: str | None = None


class DelinquencyResponse(DelinquencyCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)
    resolved_at: datetime | None = None


class UnderwritingLogCreate(BaseModel):
    loan_application_id: UUID
    underwriter_id: UUID
    decision: str
    comments: str | None = None
    checklist: dict | None = None


class UnderwritingLogUpdate(BaseModel):
    decision: str | None = None
    comments: str | None = None
    checklist: dict | None = None


class UnderwritingLogResponse(UnderwritingLogCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)


class RiskMitigationRuleCreate(BaseModel):
    name: str
    rule_code: str
    condition_expression: str
    mitigation_action: str
    priority: int
    is_active: bool = True


class RiskMitigationRuleUpdate(BaseModel):
    name: str | None = None
    condition_expression: str | None = None
    mitigation_action: str | None = None
    priority: int | None = None
    is_active: bool | None = None


class RiskMitigationRuleResponse(RiskMitigationRuleCreate, AuditResponseMixin):
    model_config = ConfigDict(from_attributes=True)
