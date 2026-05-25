from app.controllers.amortization_schedule_controller import router as amortization_schedule_router
from app.controllers.approved_loan_controller import router as approved_loan_router
from app.controllers.audit_log_controller import router as audit_log_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.collateral_controller import router as collateral_router
from app.controllers.credit_score_controller import router as credit_score_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.delinquency_controller import router as delinquency_router
from app.controllers.file_controller import router as file_router
from app.controllers.financial_profile_controller import router as financial_profile_router
from app.controllers.guarantor_controller import router as guarantor_router
from app.controllers.health_controller import router as health_router
from app.controllers.loan_application_controller import router as loan_application_router
from app.controllers.loan_product_controller import router as loan_product_router
from app.controllers.notification_controller import router as notification_router
from app.controllers.permission_controller import router as permission_router
from app.controllers.repayment_controller import router as repayment_router
from app.controllers.risk_assessment_controller import router as risk_assessment_router
from app.controllers.role_permission_controller import router as role_permission_router
from app.controllers.risk_mitigation_rule_controller import router as risk_mitigation_rule_router
from app.controllers.role_controller import router as role_router
from app.controllers.user_role_controller import router as user_role_router
from app.controllers.setting_controller import router as setting_router
from app.controllers.underwriting_log_controller import router as underwriting_log_router
from app.controllers.user_controller import router as user_router
from app.controllers.ws_controller import router as ws_router
from app.controllers.prediction_controller import router as prediction_router

api_routers = [
    auth_router,
    user_router,
    role_router,
    permission_router,
    user_role_router,
    role_permission_router,
    audit_log_router,
    notification_router,
    setting_router,
    file_router,
    customer_router,
    financial_profile_router,
    credit_score_router,
    loan_product_router,
    loan_application_router,
    risk_assessment_router,
    collateral_router,
    guarantor_router,
    approved_loan_router,
    amortization_schedule_router,
    repayment_router,
    delinquency_router,
    underwriting_log_router,
    risk_mitigation_rule_router,
    prediction_router,
]
