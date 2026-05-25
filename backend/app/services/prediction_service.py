"""
Loads the trained XGBoost models from disk and exposes a single predict() method.

The models are loaded once at module import time (singleton pattern) so that
every HTTP request reuses the same in-memory objects — no repeated disk I/O.
"""

import os
import joblib
import numpy as np
import pandas as pd

from app.schemas.prediction import LoanPredictionRequest, LoanPredictionResponse

_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "models")
_CLF_PATH = os.path.join(_BASE, "loan_classifier.pkl")
_REG_PATH = os.path.join(_BASE, "loan_regressor.pkl")
_ENC_PATH = os.path.join(_BASE, "label_encoders.pkl")
_META_PATH = os.path.join(_BASE, "model_metadata.pkl")

FEATURE_COLS = [
    "age", "annual_income", "monthly_expenses",
    "employment_status", "contract_type",
    "existing_debt", "requested_amount", "term_months",
    "credit_score", "num_dependents", "has_property",
    "previous_defaults", "debt_to_income_ratio", "loan_to_income_ratio",
]
CATEGORICAL_COLS = ["employment_status", "contract_type"]


def _load_models():
    """Load models from disk. Raises a clear error if not trained yet."""
    missing = [p for p in [_CLF_PATH, _REG_PATH, _ENC_PATH, _META_PATH]
               if not os.path.exists(p)]
    if missing:
        raise RuntimeError(
            "ML models not found. Please run: python -m ml.train_model\n"
            f"Missing: {missing}"
        )
    clf = joblib.load(_CLF_PATH)
    reg = joblib.load(_REG_PATH)
    encoders = joblib.load(_ENC_PATH)
    meta = joblib.load(_META_PATH)
    return clf, reg, encoders, meta


# Load once on module import
try:
    _clf, _reg, _encoders, _meta = _load_models()
    _models_ready = True
except RuntimeError:
    _clf = _reg = _encoders = _meta = None
    _models_ready = False


def _build_feature_row(req: LoanPredictionRequest) -> pd.DataFrame:
    monthly_income = req.annual_income / 12
    monthly_debt_payment = req.existing_debt / 60  # assume 5-yr payoff
    dti = (req.monthly_expenses + monthly_debt_payment) / (monthly_income + 1e-6)
    dti = min(max(dti, 0.0), 1.5)

    lti = req.requested_amount / (req.annual_income + 1e-6)

    row = {
        "age": req.age,
        "annual_income": req.annual_income,
        "monthly_expenses": req.monthly_expenses,
        "employment_status": req.employment_status,
        "contract_type": req.contract_type,
        "existing_debt": req.existing_debt,
        "requested_amount": req.requested_amount,
        "term_months": req.term_months,
        "credit_score": req.credit_score,
        "num_dependents": req.num_dependents,
        "has_property": int(req.has_property),
        "previous_defaults": req.previous_defaults,
        "debt_to_income_ratio": round(dti, 4),
        "loan_to_income_ratio": round(lti, 4),
    }
    return pd.DataFrame([row])


def _encode(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in CATEGORICAL_COLS:
        le = _encoders[col]
        # Handle unseen labels gracefully
        val = df[col].astype(str).iloc[0]
        if val not in le.classes_:
            val = le.classes_[0]
        df[col] = le.transform([val])
    return df


def _risk_level(prob: float) -> str:
    if prob >= 0.70:
        return "Low"
    if prob >= 0.45:
        return "Medium"
    return "High"


def _build_factors(req: LoanPredictionRequest, dti: float, lti: float) -> dict:
    """Return a human-readable dictionary of the most impactful decision factors."""
    factors = {}

    # Credit score
    if req.credit_score >= 700:
        factors["credit_score"] = f"Good ({req.credit_score}) — positive"
    elif req.credit_score >= 600:
        factors["credit_score"] = f"Fair ({req.credit_score}) — neutral"
    else:
        factors["credit_score"] = f"Poor ({req.credit_score}) — negative"

    # DTI
    if dti < 0.30:
        factors["debt_to_income_ratio"] = f"{dti:.2%} — healthy"
    elif dti < 0.45:
        factors["debt_to_income_ratio"] = f"{dti:.2%} — acceptable"
    else:
        factors["debt_to_income_ratio"] = f"{dti:.2%} — too high"

    # Employment
    emp_labels = {
        "employed": "Stable employment — positive",
        "self_employed": "Self-employed — slightly positive",
        "retired": "Retired — neutral",
        "part_time": "Part-time — slightly negative",
        "unemployed": "Unemployed — very negative",
    }
    factors["employment_status"] = emp_labels.get(req.employment_status, req.employment_status)

    # Previous defaults
    if req.previous_defaults == 0:
        factors["previous_defaults"] = "No defaults — positive"
    else:
        factors["previous_defaults"] = f"{req.previous_defaults} default(s) — negative"

    # Loan-to-income
    if lti < 3:
        factors["loan_to_income_ratio"] = f"{lti:.1f}x income — low risk"
    elif lti < 5:
        factors["loan_to_income_ratio"] = f"{lti:.1f}x income — moderate"
    else:
        factors["loan_to_income_ratio"] = f"{lti:.1f}x income — high risk"

    # Property
    factors["has_property"] = "Owns property — collateral positive" if req.has_property else "No property — neutral"

    return factors


def predict(req: LoanPredictionRequest) -> LoanPredictionResponse:
    if not _models_ready:
        raise RuntimeError(
            "ML models are not loaded. Run 'python -m ml.train_model' first."
        )

    df = _build_feature_row(req)
    dti = float(df["debt_to_income_ratio"].iloc[0])
    lti = float(df["loan_to_income_ratio"].iloc[0])

    df_enc = _encode(df)
    X = df_enc[FEATURE_COLS]

    approval_prob = float(_clf.predict_proba(X)[0][1])
    loan_approved = bool(approval_prob >= 0.50)
    max_loan_amount = float(_reg.predict(X)[0])
    max_loan_amount = round(max(0.0, max_loan_amount), 2)

    return LoanPredictionResponse(
        loan_approved=loan_approved,
        approval_probability=round(approval_prob, 4),
        max_loan_amount=max_loan_amount,
        risk_level=_risk_level(approval_prob),
        model_version=_meta["version"],
        factors=_build_factors(req, dti, lti),
    )
