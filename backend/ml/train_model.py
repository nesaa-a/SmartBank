"""
Trains two XGBoost models:
  1. Classifier  -> loan_approved (0 or 1)
  2. Regressor   -> max_loan_amount (float)

Both are saved to ml/models/ with joblib so the FastAPI backend can load them.

Why XGBoost?
  - Handles mixed data types (numeric + categorical after encoding) well
  - Robust to outliers and skewed distributions (common in financial data)
  - Strong out-of-the-box performance with minimal hyperparameter tuning
  - Fast inference — important for a real-time web endpoint
  - Interpretable via feature importance scores

Run from the backend/ directory:
    python -m ml.train_model
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor

from ml.generate_dataset import generate_dataset

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_VERSION = "1.0.0"

CATEGORICAL_COLS = ["employment_status", "contract_type"]
FEATURE_COLS = [
    "age",
    "annual_income",
    "monthly_expenses",
    "employment_status",
    "contract_type",
    "existing_debt",
    "requested_amount",
    "term_months",
    "credit_score",
    "num_dependents",
    "has_property",
    "previous_defaults",
    "debt_to_income_ratio",
    "loan_to_income_ratio",
]
TARGET_APPROVED = "loan_approved"
TARGET_AMOUNT = "max_loan_amount"


def encode_categoricals(df: pd.DataFrame, encoders: dict | None = None):
    """Label-encode categorical columns. Returns (df_encoded, encoders_dict)."""
    df = df.copy()
    if encoders is None:
        encoders = {}
    for col in CATEGORICAL_COLS:
        if col not in encoders:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
        else:
            df[col] = encoders[col].transform(df[col].astype(str))
    return df, encoders


def train():
    print("=" * 60)
    print("SmartBank Loan Prediction — Model Training")
    print("=" * 60)

    # ── 1. Generate (or load) dataset ─────────────────────────────
    csv_path = os.path.join(os.path.dirname(__file__), "loan_dataset.csv")
    if os.path.exists(csv_path):
        print(f"\nLoading existing dataset from {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print("\nGenerating synthetic dataset …")
        df = generate_dataset()
        df.to_csv(csv_path, index=False)
        print(f"Dataset saved -> {csv_path}")

    print(f"Rows: {len(df)}  |  Approval rate: {df[TARGET_APPROVED].mean():.1%}")

    # ── 2. Encode categoricals ─────────────────────────────────────
    df_enc, encoders = encode_categoricals(df)

    X = df_enc[FEATURE_COLS]
    y_cls = df_enc[TARGET_APPROVED]
    y_reg = df_enc[TARGET_AMOUNT]

    X_train, X_test, y_cls_train, y_cls_test, y_reg_train, y_reg_test = (
        train_test_split(X, y_cls, y_reg, test_size=0.20, random_state=42)
    )

    # ── 3. Train classifier ────────────────────────────────────────
    print("\n[1/2] Training XGBoost Classifier (loan_approved) …")
    clf = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_cls_train,
            eval_set=[(X_test, y_cls_test)],
            verbose=False)

    y_pred_cls = clf.predict(X_test)
    acc = accuracy_score(y_cls_test, y_pred_cls)
    cv_scores = cross_val_score(clf, X, y_cls, cv=5, scoring="accuracy")
    print(f"  Test accuracy : {acc:.4f}")
    print(f"  5-fold CV     : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"\n{classification_report(y_cls_test, y_pred_cls, target_names=['Rejected','Approved'])}")

    # Feature importance
    importances = dict(zip(FEATURE_COLS, clf.feature_importances_))
    top = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:6]
    print("  Top features:", ", ".join(f"{k}({v:.3f})" for k, v in top))

    # ── 4. Train regressor ─────────────────────────────────────────
    print("\n[2/2] Training XGBoost Regressor (max_loan_amount) …")
    reg = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    )
    reg.fit(X_train, y_reg_train,
            eval_set=[(X_test, y_reg_test)],
            verbose=False)

    y_pred_reg = reg.predict(X_test)
    mae = mean_absolute_error(y_reg_test, y_pred_reg)
    r2 = r2_score(y_reg_test, y_pred_reg)
    print(f"  MAE : {mae:,.2f}")
    print(f"  R²  : {r2:.4f}")

    # ── 5. Save models ─────────────────────────────────────────────
    os.makedirs(MODELS_DIR, exist_ok=True)
    clf_path = os.path.join(MODELS_DIR, "loan_classifier.pkl")
    reg_path = os.path.join(MODELS_DIR, "loan_regressor.pkl")
    enc_path = os.path.join(MODELS_DIR, "label_encoders.pkl")
    meta_path = os.path.join(MODELS_DIR, "model_metadata.pkl")

    joblib.dump(clf, clf_path)
    joblib.dump(reg, reg_path)
    joblib.dump(encoders, enc_path)
    joblib.dump({
        "version": MODEL_VERSION,
        "feature_cols": FEATURE_COLS,
        "categorical_cols": CATEGORICAL_COLS,
        "classifier_accuracy": float(acc),
        "regressor_mae": float(mae),
        "regressor_r2": float(r2),
    }, meta_path)

    print(f"\nModels saved to {MODELS_DIR}/")
    print(f"  loan_classifier.pkl  — approval classifier")
    print(f"  loan_regressor.pkl   — max amount regressor")
    print(f"  label_encoders.pkl   — categorical encoders")
    print(f"  model_metadata.pkl   — version & metrics")
    print("\nTraining complete.")
    return clf, reg, encoders


if __name__ == "__main__":
    train()
