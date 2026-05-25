"""
Generates a realistic synthetic loan application dataset for ML training.

Logic summary:
  - Approval is driven by credit score, DTI ratio, employment, previous defaults,
    loan-to-income ratio, and property ownership.
  - max_loan_amount is calculated as a fraction of annual income adjusted by
    credit score, DTI, employment type, and property ownership.
  - Gaussian noise is added to make the dataset imperfect, as real data would be.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ROWS = 6000

np.random.seed(RANDOM_SEED)

EMPLOYMENT_STATUSES = ["employed", "self_employed", "unemployed", "retired", "part_time"]
EMPLOYMENT_WEIGHTS = [0.50, 0.20, 0.08, 0.12, 0.10]

CONTRACT_TYPES = ["permanent", "temporary", "contract", "freelance"]
CONTRACT_WEIGHTS = [0.50, 0.20, 0.18, 0.12]


def generate_dataset(n: int = N_ROWS) -> pd.DataFrame:
    ages = np.random.randint(20, 70, size=n)

    employment = np.random.choice(EMPLOYMENT_STATUSES, size=n, p=EMPLOYMENT_WEIGHTS)
    contract = np.random.choice(CONTRACT_TYPES, size=n, p=CONTRACT_WEIGHTS)

    # Income depends on employment type
    income_base = {
        "employed": (35_000, 90_000),
        "self_employed": (25_000, 120_000),
        "unemployed": (0, 12_000),
        "retired": (18_000, 55_000),
        "part_time": (12_000, 35_000),
    }
    annual_income = np.array([
        np.random.uniform(*income_base[e]) for e in employment
    ]).round(2)

    monthly_income = annual_income / 12

    # Monthly expenses: 25-60% of monthly income
    expense_ratio = np.random.uniform(0.25, 0.60, size=n)
    monthly_expenses = (monthly_income * expense_ratio).round(2)

    # Existing debt: 0-40% of annual income
    existing_debt = (annual_income * np.random.uniform(0.0, 0.40, size=n)).round(2)

    # Requested amount: 0.5-6x annual income
    loan_multiplier = np.random.uniform(0.5, 6.0, size=n)
    requested_amount = (annual_income * loan_multiplier).round(2)
    requested_amount = np.clip(requested_amount, 1_000, 500_000)

    term_months = np.random.choice([12, 24, 36, 48, 60, 84, 120], size=n)

    credit_score = np.random.randint(300, 851, size=n)

    num_dependents = np.random.choice([0, 1, 2, 3, 4, 5], size=n,
                                      p=[0.30, 0.25, 0.22, 0.13, 0.06, 0.04])

    has_property = np.random.choice([0, 1], size=n, p=[0.45, 0.55])

    previous_defaults = np.random.choice([0, 1, 2, 3], size=n,
                                          p=[0.70, 0.18, 0.08, 0.04])

    # Derived features
    monthly_debt_payment = existing_debt / 60  # assume 5yr payoff
    dti = ((monthly_expenses + monthly_debt_payment) / (monthly_income + 1e-6)).round(4)
    dti = np.clip(dti, 0.0, 1.5)

    lti = (requested_amount / (annual_income + 1e-6)).round(4)

    # ── Approval score (deterministic rule, then sigmoid + noise) ────────────
    score = np.zeros(n)

    # Credit score (0-40 pts)
    score += np.where(credit_score >= 750, 40,
             np.where(credit_score >= 700, 30,
             np.where(credit_score >= 650, 20,
             np.where(credit_score >= 600, 10,
             np.where(credit_score >= 550,  0, -20)))))

    # DTI ratio (0-20 pts)
    score += np.where(dti < 0.20, 20,
             np.where(dti < 0.30, 15,
             np.where(dti < 0.40,  5,
             np.where(dti < 0.50, -10, -30))))

    # Employment (-30 to +15)
    emp_pts = {"employed": 15, "self_employed": 10, "retired": 5,
               "part_time": -5, "unemployed": -30}
    score += np.array([emp_pts[e] for e in employment])

    # Contract type (-5 to +10)
    contract_pts = {"permanent": 10, "contract": 5, "temporary": 0, "freelance": -5}
    score += np.array([contract_pts[c] for c in contract])

    # Previous defaults (-40 to +15)
    score += np.where(previous_defaults == 0, 15,
             np.where(previous_defaults == 1, -20, -40))

    # Loan-to-income (-25 to +10)
    score += np.where(lti < 2, 10,
             np.where(lti < 3,  5,
             np.where(lti < 5,  0,
             np.where(lti < 7, -10, -25))))

    # Property ownership
    score += has_property * 10

    # Age penalty at extremes
    score += np.where(ages < 21, -10, np.where(ages > 65, -5, 0))

    # Normalize to probability via sigmoid + Gaussian noise
    norm_score = (score + 100) / 220.0
    noise = np.random.normal(0, 0.07, size=n)
    approval_prob = 1 / (1 + np.exp(-6 * (norm_score + noise - 0.5)))
    approval_prob = np.clip(approval_prob, 0, 1)

    loan_approved = (approval_prob > 0.5).astype(int)

    # ── Max loan amount (only meaningful when approved, but computed always) ─
    credit_multiplier = np.where(credit_score >= 750, 4.5,
                        np.where(credit_score >= 700, 3.5,
                        np.where(credit_score >= 650, 2.5,
                        np.where(credit_score >= 600, 1.5, 0.75))))

    dti_factor = np.clip(1 - dti * 2, 0.1, 1.0)
    property_bonus = np.where(has_property == 1, 1.2, 1.0)

    emp_factor_map = {"employed": 1.0, "self_employed": 0.9,
                      "retired": 0.7, "part_time": 0.6, "unemployed": 0.2}
    emp_factor = np.array([emp_factor_map[e] for e in employment])

    max_loan_amount = (annual_income * credit_multiplier * dti_factor
                       * property_bonus * emp_factor)
    max_loan_amount = np.clip(max_loan_amount, 500, 500_000).round(2)

    # For rejected applications, cap at the computed max (which is low anyway)
    max_loan_amount = np.where(loan_approved == 0,
                               max_loan_amount * np.random.uniform(0.1, 0.5, n),
                               max_loan_amount)
    max_loan_amount = max_loan_amount.round(2)

    df = pd.DataFrame({
        "age": ages,
        "annual_income": annual_income,
        "monthly_expenses": monthly_expenses,
        "employment_status": employment,
        "contract_type": contract,
        "existing_debt": existing_debt,
        "requested_amount": requested_amount,
        "term_months": term_months,
        "credit_score": credit_score,
        "num_dependents": num_dependents,
        "has_property": has_property,
        "previous_defaults": previous_defaults,
        "debt_to_income_ratio": dti,
        "loan_to_income_ratio": lti,
        "loan_approved": loan_approved,
        "max_loan_amount": max_loan_amount,
    })

    return df


if __name__ == "__main__":
    df = generate_dataset()
    out_path = "ml/loan_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"Dataset saved -> {out_path}")
    print(f"Shape: {df.shape}")
    print(f"Approval rate: {df['loan_approved'].mean():.1%}")
    print(f"\nClass distribution:\n{df['loan_approved'].value_counts()}")
    print(f"\nSample rows:\n{df.head(3).to_string()}")
