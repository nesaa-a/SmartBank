export type EmploymentStatus = "employed" | "self_employed" | "unemployed" | "retired" | "part_time";
export type ContractType = "permanent" | "temporary" | "contract" | "freelance";
export type RiskLevel = "Low" | "Medium" | "High";

export interface LoanApplicationRequest {
  age: number;
  annual_income: number;
  monthly_expenses: number;
  employment_status: EmploymentStatus;
  contract_type: ContractType;
  existing_debt: number;
  requested_amount: number;
  term_months: number;
  credit_score: number;
  num_dependents: number;
  has_property: boolean;
  previous_defaults: number;
}

export interface LoanPredictionResult {
  loan_approved: boolean;
  approval_probability: number;
  max_loan_amount: number;
  risk_level: RiskLevel;
  model_version: string;
  factors: Record<string, string>;
}
