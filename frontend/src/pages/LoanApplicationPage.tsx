import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { User, DollarSign, Briefcase, CreditCard, Landmark, ArrowRight } from "lucide-react";
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
  { value: "12",  label: "12 months — 1 year" },
  { value: "24",  label: "24 months — 2 years" },
  { value: "36",  label: "36 months — 3 years" },
  { value: "48",  label: "48 months — 4 years" },
  { value: "60",  label: "60 months — 5 years" },
  { value: "84",  label: "84 months — 7 years" },
  { value: "120", label: "120 months — 10 years" },
];

const sections = [
  { icon: User,      label: "Personal" },
  { icon: DollarSign, label: "Financial" },
  { icon: Briefcase, label: "Employment" },
  { icon: Landmark,  label: "Loan" },
  { icon: CreditCard, label: "Credit" },
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
      sessionStorage.setItem("loan_result", JSON.stringify(result));
      sessionStorage.setItem("loan_application", JSON.stringify(data));
      navigate("/result");
    } catch {
      setApiError("Could not reach the prediction service. Please make sure the backend is running.");
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      {/* Header */}
      <div className="mb-7">
        <h1 className="text-2xl font-extrabold text-white">Loan Application</h1>
        <p className="mt-1.5 text-sm text-slate-500">
          Fill in the form below — our AI will return an instant decision.
        </p>
      </div>

      {/* Progress steps */}
      <div className="mb-7 flex items-center gap-1 overflow-x-auto pb-1">
        {sections.map(({ icon: Icon, label }, i) => (
          <div key={label} className="flex shrink-0 items-center gap-1">
            <div className="flex items-center gap-1.5 rounded-full bg-slate-800/60 border border-slate-700/50 px-3 py-1.5">
              <Icon className="h-3 w-3 text-blue-400" />
              <span className="text-xs font-medium text-slate-400">{label}</span>
            </div>
            {i < sections.length - 1 && (
              <ArrowRight className="h-3 w-3 shrink-0 text-slate-700" />
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
        {/* Personal */}
        <Card title="Personal Information" accent="blue">
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

        {/* Financial */}
        <Card title="Financial Information" accent="blue">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Input
              label="Annual Income (EUR)"
              type="number"
              placeholder="36 000"
              hint="Before tax"
              error={errors.annual_income?.message}
              required
              {...register("annual_income")}
            />
            <Input
              label="Monthly Expenses (EUR)"
              type="number"
              placeholder="1 200"
              hint="Rent, food, utilities…"
              error={errors.monthly_expenses?.message}
              required
              {...register("monthly_expenses")}
            />
            <Input
              label="Existing Debt (EUR)"
              type="number"
              placeholder="5 000"
              hint="Total outstanding debt"
              error={errors.existing_debt?.message}
              required
              {...register("existing_debt")}
            />
          </div>
        </Card>

        {/* Employment */}
        <Card title="Employment" accent="blue">
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
        <Card title="Loan Details" accent="blue">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Requested Amount (EUR)"
              type="number"
              placeholder="15 000"
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
        <Card title="Credit Profile" accent="blue">
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
              label="Own Property?"
              options={[
                { value: "true",  label: "Yes — I own property" },
                { value: "false", label: "No — renting / other" },
              ]}
              error={errors.has_property?.message}
              required
              {...register("has_property")}
            />
            <Input
              label="Previous Defaults"
              type="number"
              placeholder="0"
              hint="Number of loan defaults"
              error={errors.previous_defaults?.message}
              required
              {...register("previous_defaults")}
            />
          </div>
        </Card>

        {apiError && (
          <div className="rounded-xl border border-red-500/20 bg-red-500/8 px-4 py-3 text-sm text-red-400">
            {apiError}
          </div>
        )}

        <div className="flex gap-3 pb-8">
          <Button type="submit" size="lg" loading={isSubmitting}>
            {isSubmitting ? "Analysing your profile…" : "Submit Application"}
            {!isSubmitting && <ArrowRight className="h-4 w-4" />}
          </Button>
          <Button type="button" variant="secondary" size="lg" onClick={() => navigate("/dashboard")}>
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
}
