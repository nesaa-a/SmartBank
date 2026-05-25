import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircle, XCircle, AlertTriangle, ArrowRight, RotateCcw } from "lucide-react";
import type { LoanPredictionResult } from "../types/loan";
import { formatCurrency, formatPercent } from "../utils/formatters";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";

const riskBadge: Record<string, "green" | "yellow" | "red"> = {
  Low: "green",
  Medium: "yellow",
  High: "red",
};

export function LoanResultPage() {
  const navigate = useNavigate();
  const [result, setResult] = useState<LoanPredictionResult | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("loan_result");
    if (!stored) {
      navigate("/apply");
      return;
    }
    setResult(JSON.parse(stored));
  }, []);

  if (!result) return null;

  const approved = result.loan_approved;
  const pct = Math.round(result.approval_probability * 100);

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Application Result</h1>
        <p className="mt-1 text-sm text-gray-500">
          Model version {result.model_version} — instant AI decision
        </p>
      </div>

      {/* Decision banner */}
      <div
        className={`mb-6 flex items-center gap-4 rounded-2xl p-6 ${
          approved ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"
        }`}
      >
        {approved ? (
          <CheckCircle className="h-12 w-12 shrink-0 text-green-600" />
        ) : (
          <XCircle className="h-12 w-12 shrink-0 text-red-500" />
        )}
        <div>
          <p className={`text-xl font-bold ${approved ? "text-green-800" : "text-red-700"}`}>
            {approved ? "Likely Approved" : "Likely Rejected"}
          </p>
          <p className={`mt-0.5 text-sm ${approved ? "text-green-700" : "text-red-600"}`}>
            The model is {pct}% confident in this decision.
          </p>
        </div>
        <div className="ml-auto text-right">
          <Badge label={result.risk_level + " Risk"} variant={riskBadge[result.risk_level]} />
        </div>
      </div>

      {/* Key numbers */}
      <div className="mb-6 grid grid-cols-2 gap-4">
        <Card>
          <p className="text-sm font-medium text-gray-500">Approval Probability</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">{formatPercent(result.approval_probability)}</p>

          {/* Visual bar */}
          <div className="mt-3 h-2 w-full rounded-full bg-gray-200">
            <div
              className={`h-2 rounded-full transition-all ${approved ? "bg-green-500" : "bg-red-400"}`}
              style={{ width: `${pct}%` }}
            />
          </div>
        </Card>

        <Card>
          <p className="text-sm font-medium text-gray-500">Max Eligible Amount</p>
          <p className="mt-1 text-3xl font-bold text-gray-900">
            {formatCurrency(result.max_loan_amount)}
          </p>
          <p className="mt-1 text-xs text-gray-400">Recommended maximum by the model</p>
        </Card>
      </div>

      {/* Decision factors */}
      <Card title="Decision Factors" className="mb-6">
        <p className="mb-4 text-sm text-gray-500">
          The following factors had the most influence on this decision:
        </p>
        <ul className="flex flex-col gap-3">
          {Object.entries(result.factors).map(([key, value]) => {
            const isPositive = value.toLowerCase().includes("positive") || value.toLowerCase().includes("healthy") || value.toLowerCase().includes("good") || value.toLowerCase().includes("low risk") || value.toLowerCase().includes("no defaults") || value.toLowerCase().includes("collateral");
            const isNegative = value.toLowerCase().includes("negative") || value.toLowerCase().includes("too high") || value.toLowerCase().includes("poor") || value.toLowerCase().includes("high risk");
            return (
              <li key={key} className="flex items-start gap-3">
                {isNegative ? (
                  <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" />
                ) : isPositive ? (
                  <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                ) : (
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-yellow-500" />
                )}
                <div>
                  <span className="text-sm font-medium text-gray-700 capitalize">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="ml-2 text-sm text-gray-500">{value}</span>
                </div>
              </li>
            );
          })}
        </ul>
      </Card>

      {/* Disclaimer */}
      <div className="mb-8 rounded-lg border border-yellow-200 bg-yellow-50 px-4 py-3 text-xs text-yellow-800">
        <strong>Disclaimer:</strong> This is an AI-generated estimate for informational purposes only.
        Final loan decisions are made by human underwriters and may differ from this prediction.
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3 pb-8">
        <Button onClick={() => navigate("/apply")}>
          <RotateCcw className="h-4 w-4" />
          Apply Again
        </Button>
        <Button variant="secondary" onClick={() => navigate("/dashboard")}>
          Back to Dashboard
          <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
