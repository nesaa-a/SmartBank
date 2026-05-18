import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base


class LoanApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class RiskLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ApprovedLoanStatus(str, enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DEFAULTED = "defaulted"
    RESTRUCTURED = "restructured"


class DelinquencySeverity(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Customer(Base, AuditMixin):
    __tablename__ = "customers"

    customer_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    national_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    financial_profiles: Mapped[list["FinancialProfile"]] = relationship(back_populates="customer")
    credit_scores: Mapped[list["CreditScore"]] = relationship(back_populates="customer")
    loan_applications: Mapped[list["LoanApplication"]] = relationship(back_populates="customer")


class FinancialProfile(Base, AuditMixin):
    __tablename__ = "financial_profiles"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    annual_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    employment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    employer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    monthly_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    total_assets: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    total_liabilities: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    debt_to_income_ratio: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="financial_profiles")


class CreditScore(Base, AuditMixin):
    __tablename__ = "credit_scores"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    bureau: Mapped[str] = mapped_column(String(100), nullable=False)
    report_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    risk_grade: Mapped[str] = mapped_column(String(10), nullable=False)
    factors: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="credit_scores")


class LoanProduct(Base, AuditMixin):
    __tablename__ = "loan_products"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    term_months_min: Mapped[int] = mapped_column(Integer, nullable=False)
    term_months_max: Mapped[int] = mapped_column(Integer, nullable=False)
    min_credit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_loan_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    loan_applications: Mapped[list["LoanApplication"]] = relationship(back_populates="loan_product")


class LoanApplication(Base, AuditMixin):
    __tablename__ = "loan_applications"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    loan_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    application_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    requested_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[LoanApplicationStatus] = mapped_column(
        Enum(LoanApplicationStatus, name="loan_application_status"),
        nullable=False,
        default=LoanApplicationStatus.DRAFT,
        index=True,
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="loan_applications")
    loan_product: Mapped["LoanProduct"] = relationship(back_populates="loan_applications")
    risk_assessments: Mapped[list["RiskAssessment"]] = relationship(back_populates="loan_application")
    collaterals: Mapped[list["Collateral"]] = relationship(back_populates="loan_application")
    guarantors: Mapped[list["Guarantor"]] = relationship(back_populates="loan_application")
    approved_loan: Mapped["ApprovedLoan | None"] = relationship(back_populates="loan_application", uselist=False)
    underwriting_logs: Mapped[list["UnderwritingLog"]] = relationship(back_populates="loan_application")


class RiskAssessment(Base, AuditMixin):
    __tablename__ = "risk_assessments"

    loan_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level"),
        nullable=False,
        index=True,
    )
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    factors: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    assessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="risk_assessments")


class Collateral(Base, AuditMixin):
    __tablename__ = "collaterals"

    loan_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    collateral_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    valuation_date: Mapped[date] = mapped_column(Date, nullable=False)

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="collaterals")


class Guarantor(Base, AuditMixin):
    __tablename__ = "guarantors"

    loan_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False)
    annual_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(30), nullable=False)

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="guarantors")


class ApprovedLoan(Base, AuditMixin):
    __tablename__ = "approved_loans"
    __table_args__ = (UniqueConstraint("loan_application_id", name="uq_approved_loans_application"),)

    loan_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_applications.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    approved_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    disbursement_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[ApprovedLoanStatus] = mapped_column(
        Enum(ApprovedLoanStatus, name="approved_loan_status"),
        nullable=False,
        default=ApprovedLoanStatus.ACTIVE,
        index=True,
    )

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="approved_loan")
    amortization_schedules: Mapped[list["AmortizationSchedule"]] = relationship(back_populates="approved_loan")
    repayments: Mapped[list["Repayment"]] = relationship(back_populates="approved_loan")
    delinquencies: Mapped[list["Delinquency"]] = relationship(back_populates="approved_loan")


class AmortizationSchedule(Base, AuditMixin):
    __tablename__ = "amortization_schedules"
    __table_args__ = (
        UniqueConstraint("approved_loan_id", "installment_number", name="uq_amortization_loan_installment"),
    )

    approved_loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approved_loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    installment_number: Mapped[int] = mapped_column(Integer, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    principal_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    interest_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    remaining_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    approved_loan: Mapped["ApprovedLoan"] = relationship(back_populates="amortization_schedules")


class Repayment(Base, AuditMixin):
    __tablename__ = "repayments"

    approved_loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approved_loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    approved_loan: Mapped["ApprovedLoan"] = relationship(back_populates="repayments")


class Delinquency(Base, AuditMixin):
    __tablename__ = "delinquencies"

    approved_loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approved_loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    days_overdue: Mapped[int] = mapped_column(Integer, nullable=False)
    overdue_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    severity: Mapped[DelinquencySeverity] = mapped_column(
        Enum(DelinquencySeverity, name="delinquency_severity"),
        nullable=False,
        index=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    approved_loan: Mapped["ApprovedLoan"] = relationship(back_populates="delinquencies")


class UnderwritingLog(Base, AuditMixin):
    __tablename__ = "underwriting_logs"

    loan_application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("loan_applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    underwriter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    decision: Mapped[str] = mapped_column(String(50), nullable=False)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    checklist: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    loan_application: Mapped["LoanApplication"] = relationship(back_populates="underwriting_logs")


class RiskMitigationRule(Base, AuditMixin):
    __tablename__ = "risk_mitigation_rules"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rule_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    condition_expression: Mapped[str] = mapped_column(Text, nullable=False)
    mitigation_action: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
