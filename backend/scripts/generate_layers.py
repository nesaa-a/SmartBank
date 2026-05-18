"""One-time generator for repository, service, and controller modules."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ENTITIES = [
    ("user", "User", "users"),
    ("role", "Role", "roles"),
    ("user_role", "UserRole", "user-roles"),
    ("permission", "Permission", "permissions"),
    ("role_permission", "RolePermission", "role-permissions"),
    ("refresh_token", "RefreshToken", "refresh-tokens"),
    ("audit_log", "AuditLog", "audit-logs"),
    ("notification", "Notification", "notifications"),
    ("setting", "Setting", "settings"),
    ("file", "File", "files"),
    ("customer", "Customer", "customers"),
    ("financial_profile", "FinancialProfile", "financial-profiles"),
    ("credit_score", "CreditScore", "credit-scores"),
    ("loan_product", "LoanProduct", "loan-products"),
    ("loan_application", "LoanApplication", "loan-applications"),
    ("risk_assessment", "RiskAssessment", "risk-assessments"),
    ("collateral", "Collateral", "collaterals"),
    ("guarantor", "Guarantor", "guarantors"),
    ("approved_loan", "ApprovedLoan", "approved-loans"),
    ("amortization_schedule", "AmortizationSchedule", "amortization-schedules"),
    ("repayment", "Repayment", "repayments"),
    ("delinquency", "Delinquency", "delinquencies"),
    ("underwriting_log", "UnderwritingLog", "underwriting-logs"),
    ("risk_mitigation_rule", "RiskMitigationRule", "risk-mitigation-rules"),
]

MODEL_IMPORTS = {
    "User": "app.models.auth",
    "Role": "app.models.auth",
    "UserRole": "app.models.auth",
    "Permission": "app.models.auth",
    "RolePermission": "app.models.auth",
    "RefreshToken": "app.models.auth",
    "AuditLog": "app.models.system",
    "Notification": "app.models.system",
    "Setting": "app.models.system",
    "File": "app.models.system",
}
for name in [
    "Customer",
    "FinancialProfile",
    "CreditScore",
    "LoanProduct",
    "LoanApplication",
    "RiskAssessment",
    "Collateral",
    "Guarantor",
    "ApprovedLoan",
    "AmortizationSchedule",
    "Repayment",
    "Delinquency",
    "UnderwritingLog",
    "RiskMitigationRule",
]:
    MODEL_IMPORTS[name] = "app.models.loan"

SCHEMA_IMPORTS = {
    "User": ("UserCreate", "UserUpdate", "UserResponse", "app.schemas.auth"),
    "Role": ("RoleCreate", "RoleUpdate", "RoleResponse", "app.schemas.auth"),
    "Permission": ("PermissionCreate", "PermissionUpdate", "PermissionResponse", "app.schemas.auth"),
    "AuditLog": ("AuditLogCreate", None, "AuditLogResponse", "app.schemas.system"),
    "Notification": ("NotificationCreate", "NotificationUpdate", "NotificationResponse", "app.schemas.system"),
    "Setting": ("SettingCreate", "SettingUpdate", "SettingResponse", "app.schemas.system"),
    "File": ("FileCreate", None, "FileResponse", "app.schemas.system"),
    "Customer": ("CustomerCreate", "CustomerUpdate", "CustomerResponse", "app.schemas.loan"),
    "FinancialProfile": ("FinancialProfileCreate", "FinancialProfileUpdate", "FinancialProfileResponse", "app.schemas.loan"),
    "CreditScore": ("CreditScoreCreate", "CreditScoreUpdate", "CreditScoreResponse", "app.schemas.loan"),
    "LoanProduct": ("LoanProductCreate", "LoanProductUpdate", "LoanProductResponse", "app.schemas.loan"),
    "LoanApplication": ("LoanApplicationCreate", "LoanApplicationUpdate", "LoanApplicationResponse", "app.schemas.loan"),
    "RiskAssessment": (None, None, "RiskAssessmentResponse", "app.schemas.loan"),
    "Collateral": ("CollateralCreate", "CollateralUpdate", "CollateralResponse", "app.schemas.loan"),
    "Guarantor": ("GuarantorCreate", "GuarantorUpdate", "GuarantorResponse", "app.schemas.loan"),
    "ApprovedLoan": ("ApprovedLoanCreate", "ApprovedLoanUpdate", "ApprovedLoanResponse", "app.schemas.loan"),
    "AmortizationSchedule": ("AmortizationScheduleCreate", "AmortizationScheduleUpdate", "AmortizationScheduleResponse", "app.schemas.loan"),
    "Repayment": ("RepaymentCreate", "RepaymentUpdate", "RepaymentResponse", "app.schemas.loan"),
    "Delinquency": ("DelinquencyCreate", "DelinquencyUpdate", "DelinquencyResponse", "app.schemas.loan"),
    "UnderwritingLog": ("UnderwritingLogCreate", "UnderwritingLogUpdate", "UnderwritingLogResponse", "app.schemas.loan"),
    "RiskMitigationRule": ("RiskMitigationRuleCreate", "RiskMitigationRuleUpdate", "RiskMitigationRuleResponse", "app.schemas.loan"),
}

SKIP_CRUD = {"UserRole", "RolePermission", "RefreshToken", "RiskAssessment"}


def repo_file(snake: str, model: str) -> str:
    mod = MODEL_IMPORTS[model]
    class_name = "".join(part.capitalize() for part in snake.split("_")) + "Repository"
    return f'''from {mod} import {model}
from app.repositories.base import BaseRepository


class {class_name}(BaseRepository[{model}]):
    model = {model}
'''


def service_file(snake: str, model: str, route: str) -> str:
    if model in SKIP_CRUD and model != "LoanApplication":
        return ""
    repo_class = "".join(part.capitalize() for part in snake.split("_")) + "Repository"
    service_class = model + "Service"
    schema = SCHEMA_IMPORTS.get(model)
    if not schema:
        return ""
    create_schema, update_schema, response_schema, schema_mod = schema
    lines = [
        f"from uuid import UUID",
        f"",
        f"from sqlalchemy.ext.asyncio import AsyncSession",
        f"",
        f"from {MODEL_IMPORTS[model]} import {model}",
        f"from app.repositories.{snake}_repository import {repo_class}",
        f"from {schema_mod} import {response_schema}",
    ]
    if create_schema:
        lines.append(f"from {schema_mod} import {create_schema}")
    if update_schema:
        lines.append(f"from {schema_mod} import {update_schema}")

    body = [
        f"",
        f"class {service_class}:",
        f"    def __init__(self, session: AsyncSession) -> None:",
        f"        self.repo = {repo_class}(session)",
        f"        self.session = session",
        f"",
        f"    async def get(self, entity_id: UUID) -> {model} | None:",
        f"        return await self.repo.get_by_id(entity_id)",
        f"",
        f"    async def list(self, skip: int = 0, limit: int = 50) -> list[{model}]:",
        f"        return await self.repo.list(skip=skip, limit=limit)",
        f"",
        f"    async def count(self) -> int:",
        f"        return await self.repo.count()",
    ]
    if create_schema:
        body.extend(
            [
                f"",
                f"    async def create(self, payload: {create_schema}, actor_id: UUID | None = None) -> {model}:",
                f"        entity = {model}(**payload.model_dump(), created_by=actor_id, updated_by=actor_id)",
                f"        return await self.repo.create(entity)",
            ]
        )
    if update_schema:
        body.extend(
            [
                f"",
                f"    async def update(self, entity_id: UUID, payload: {update_schema}, actor_id: UUID | None = None) -> {model} | None:",
                f"        entity = await self.repo.get_by_id(entity_id)",
                f"        if entity is None:",
                f"            return None",
                f"        return await self.repo.update(entity, payload.model_dump(exclude_unset=True), updated_by=actor_id)",
            ]
        )
    body.extend(
        [
            f"",
            f"    async def delete(self, entity_id: UUID) -> bool:",
            f"        entity = await self.repo.get_by_id(entity_id)",
            f"        if entity is None:",
            f"            return False",
            f"        await self.repo.delete(entity)",
            f"        return True",
        ]
    )
    return "\n".join(lines + body) + "\n"


def controller_file(snake: str, model: str, route: str) -> str:
    if model in SKIP_CRUD and model != "LoanApplication":
        return ""
    schema = SCHEMA_IMPORTS.get(model)
    if not schema:
        return ""
    create_schema, update_schema, response_schema, schema_mod = schema
    service_class = model + "Service"
    router_var = route.replace("-", "_") + "_router"

    lines = [
        f"from uuid import UUID",
        f"",
        f"from fastapi import APIRouter, Depends, HTTPException, status",
        f"from sqlalchemy.ext.asyncio import AsyncSession",
        f"",
        f"from app.core.database import get_db",
        f"from app.core.dependencies import get_current_user",
        f"from app.models.auth import User",
        f"from {schema_mod} import {response_schema}",
        f"from app.schemas.common import PaginatedResponse",
        f"from app.services.{snake}_service import {service_class}",
    ]
    if create_schema:
        lines.append(f"from {schema_mod} import {create_schema}")
    if update_schema:
        lines.append(f"from {schema_mod} import {update_schema}")

    lines.extend(
        [
            f"",
            f"router = APIRouter(prefix=\"/{route}\", tags=[\"{route}\"])",
            f"",
            f"@router.get(\"\", response_model=PaginatedResponse[{response_schema}])",
            f"async def list_{snake}(",
            f"    skip: int = 0,",
            f"    limit: int = 50,",
            f"    session: AsyncSession = Depends(get_db),",
            f"    current_user: User = Depends(get_current_user),",
            f"):",
            f"    service = {service_class}(session)",
            f"    items = await service.list(skip=skip, limit=limit)",
            f"    total = await service.count()",
            f"    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)",
            f"",
            f"@router.get(\"/{{entity_id}}\", response_model={response_schema})",
            f"async def get_{snake}(",
            f"    entity_id: UUID,",
            f"    session: AsyncSession = Depends(get_db),",
            f"    current_user: User = Depends(get_current_user),",
            f"):",
            f"    service = {service_class}(session)",
            f"    entity = await service.get(entity_id)",
            f"    if entity is None:",
            f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Not found\")",
            f"    return entity",
        ]
    )
    if create_schema:
        lines.extend(
            [
                f"",
                f"@router.post(\"\", response_model={response_schema}, status_code=status.HTTP_201_CREATED)",
                f"async def create_{snake}(",
                f"    payload: {create_schema},",
                f"    session: AsyncSession = Depends(get_db),",
                f"    current_user: User = Depends(get_current_user),",
                f"):",
                f"    service = {service_class}(session)",
                f"    return await service.create(payload, actor_id=current_user.id)",
            ]
        )
    if update_schema:
        lines.extend(
            [
                f"",
                f"@router.patch(\"/{{entity_id}}\", response_model={response_schema})",
                f"async def update_{snake}(",
                f"    entity_id: UUID,",
                f"    payload: {update_schema},",
                f"    session: AsyncSession = Depends(get_db),",
                f"    current_user: User = Depends(get_current_user),",
                f"):",
                f"    service = {service_class}(session)",
                f"    entity = await service.update(entity_id, payload, actor_id=current_user.id)",
                f"    if entity is None:",
                f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Not found\")",
                f"    return entity",
            ]
        )
    lines.extend(
        [
            f"",
            f"@router.delete(\"/{{entity_id}}\", status_code=status.HTTP_204_NO_CONTENT)",
            f"async def delete_{snake}(",
            f"    entity_id: UUID,",
            f"    session: AsyncSession = Depends(get_db),",
            f"    current_user: User = Depends(get_current_user),",
            f"):",
            f"    service = {service_class}(session)",
            f"    deleted = await service.delete(entity_id)",
            f"    if not deleted:",
            f"        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Not found\")",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    for snake, model, route in ENTITIES:
        (ROOT / "app" / "repositories" / f"{snake}_repository.py").write_text(
            repo_file(snake, model), encoding="utf-8"
        )
        svc = service_file(snake, model, route)
        if svc:
            (ROOT / "app" / "services" / f"{snake}_service.py").write_text(svc, encoding="utf-8")
        ctrl = controller_file(snake, model, route)
        if ctrl:
            (ROOT / "app" / "controllers" / f"{snake}_controller.py").write_text(ctrl, encoding="utf-8")

    print("Generated repository, service, and controller modules.")


if __name__ == "__main__":
    main()
