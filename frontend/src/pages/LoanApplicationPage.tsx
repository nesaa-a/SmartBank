import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { loanService } from "../services/loanService";
import type { LoanPredictionResult } from "../types/loan";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";

const schema = z.object({
  age: z.coerce.number().int().min(18, "Must be 18+").max(100),
  annual_income: z.coerce.number().positive("Must be positive"),
  monthly_expenses: z.coerce.number().min(0),
  employment_status: z.enum(["employed", "self_employed", "unemployed", "retired", "part_time"]),
  contract_type: z.enum(["permanent", "temporary", "contract", "freelance"]),
  existing_debt: z.coerce.number().min(0),
  requested_amount: z.coerce.number().positive("Must be positive"),
  term_months: z.coerce.number().int().min(6).max(360),
  credit_score: z.coerce.number().int().min(300).max(850),
  num_dependents: z.coerce.number().int().min(0),
  has_property: z.enum(["true", "false"]),
  previous_defaults: z.coerce.number().int().min(0),
});


const EMPLOYMENT_OPTIONS = [
  { value: "employed",      label: "Employed (full-time)" },
  { value: "self_employed", label: "Self-employed" },
  { value: "unemployed",    label: "Unemployed" },
  { value: "retired",       label: "Retired" },
  { value: "part_time",     label: "Part-time" },
];

const CONTRACT_OPTIONS = [
  { value: "permanent",  label: "Permanent contract" },
  { value: "temporary",  label: "Temporary contract" },
  { value: "contract",   label: "Fixed-term contract" },
  { value: "freelance",  label: "Freelance / Gig" },
];

const TERM_OPTIONS = [
  { value: "12",  label: "12 months (1 year)" },
  { value: "24",  label: "24 months (2 years)" },
  { value: "36",  label: "36 months (3 years)" },
  { value: "48",  label: "48 months (4 years)" },
  { value: "60",  label: "60 months (5 years)" },
  { value: "84",  label: "84 months (7 years)" },
  { value: "120", label: "120 months (10 years)" },
];

export function LoanApplicationPage() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<z.input<typeof schema>, unknown, z.output<typeof schema>>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: z.output<typeof schema>) {
    setApiError("");
    try {
      const result: LoanPredictionResult = await loanService.predict({
        ...data,
        has_property: data.has_property === "true",
      });
      // Store result in sessionStorage and navigate to result page
      sessionStorage.setItem("loan_result", JSON.stringify(result));
      sessionStorage.setItem("loan_application", JSON.stringify(data));
      navigate("/result");
    } catch {
      setApiError("Could not reach the prediction service. Please make sure the backend is running.");
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Loan Application</h1>
        <p className="mt-1 text-sm text-gray-500">
          Fill in the form below. Our AI will assess your application and return an instant decision.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6">
        {/* Personal Information */}
        <Card title="Personal Information">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Age"
              type="number"
              placeholder="30"
              hint="Must be 18 or older"
              error={errors.age?.message}
              required
              {...register("age")}
            />
            <Input
              label="Number of Dependents"
              type="number"
              placeholder="0"
              hint="Children, elderly relatives, etc."
              error={errors.num_dependents?.message}
              required
              {...register("num_dependents")}
            />
          </div>
        </Card>

        {/* Financial Information */}
        <Card title="Financial Information">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Input
              label="Annual Income (EUR)"
              type="number"
              placeholder="36000"
              hint="Before tax"
              error={errors.annual_income?.message}
              required
              {...register("annual_income")}
            />
            <Input
              label="Monthly Expenses (EUR)"
              type="number"
              placeholder="1200"
              hint="Rent, food, utilities, etc."
              error={errors.monthly_expenses?.message}
              required
              {...register("monthly_expenses")}
            />
            <Input
              label="Existing Debt (EUR)"
              type="number"
              placeholder="5000"
              hint="Total outstanding loans / credit"
              error={errors.existing_debt?.message}
              required
              {...register("existing_debt")}
            />
          </div>
        </Card>

        {/* Employment */}
        <Card title="Employment">
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Employment Status"
              options={EMPLOYMENT_OPTIONS}
              error={errors.employment_status?.message}
              required
              {...register("employment_status")}
            />
            <Select
              label="Contract Type"
              options={CONTRACT_OPTIONS}
              error={errors.contract_type?.message}
              required
              {...register("contract_type")}
            />
          </div>
        </Card>

        {/* Loan Details */}
        <Card title="Loan Details">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Requested Amount (EUR)"
              type="number"
              placeholder="15000"
              error={errors.requested_amount?.message}
              required
              {...register("requested_amount")}
            />
            <Select
              label="Loan Duration"
              options={TERM_OPTIONS}
              error={errors.term_months?.message}
              required
              {...register("term_months")}
            />
          </div>
        </Card>

        {/* Credit Profile */}
        <Card title="Credit Profile">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Input
              label="Credit Score"
              type="number"
              placeholder="720"
              hint="300 (poor) – 850 (excellent)"
              error={errors.credit_score?.message}
              required
              {...register("credit_score")}
            />
            <Select
              label="Do you own property?"
              options={[
                { value: "true",  label: "Yes — I own property" },
                { value: "false", label: "No — I rent / other" },
              ]}
              error={errors.has_property?.message}
              required
              {...register("has_property")}
            />
            <Input
              label="Previous Loan Defaults"
              type="number"
              placeholder="0"
              hint="Number of times you defaulted"
              error={errors.previous_defaults?.message}
              required
              {...register("previous_defaults")}
            />
          </div>
        </Card>

        {apiError && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {apiError}
          </div>
        )}

        <div className="flex gap-3 pb-8">
          <Button type="submit" size="lg" loading={isSubmitting}>
            {isSubmitting ? "Analysing…" : "Submit Application"}
          </Button>
          <Button type="button" variant="secondary" size="lg" onClick={() => navigate("/dashboard")}>
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
}
