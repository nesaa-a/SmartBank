import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CheckCircle, XCircle, AlertTriangle, ArrowRight, RotateCcw, TrendingUp, Banknote } from "lucide-react";
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
    if (!stored) { navigate("/apply"); return; }
    setResult(JSON.parse(stored));
  }, []);

  if (!result) return null;

  const approved = result.loan_approved;
  const pct = Math.round(result.approval_probability * 100);

  return (
    <div className="mx-auto max-w-2xl animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-extrabold text-white">Application Result</h1>
        <p className="mt-1 text-xs text-slate-600 font-mono">
          Model v{result.model_version} · Instant AI decision
        </p>
      </div>

      {/* Decision banner */}
      <div
        className={`relative mb-5 overflow-hidden rounded-2xl border p-6 ${
          approved
            ? "bg-gradient-to-br from-emerald-950/60 to-slate-950 border-emerald-500/25"
            : "bg-gradient-to-br from-red-950/60 to-slate-950 border-red-500/25"
        }`}
      >
        <div className="pointer-events-none absolute right-0 top-0 h-full w-1/3 bg-gradient-to-l from-white/[0.02] to-transparent" />
        <div className="flex items-center gap-5">
          <div className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl shadow-lg ${
            approved
              ? "bg-emerald-500/15 ring-1 ring-emerald-500/30 shadow-emerald-900/30"
              : "bg-red-500/15 ring-1 ring-red-500/30 shadow-red-900/30"
          }`}>
            {approved
              ? <CheckCircle className="h-7 w-7 text-emerald-400" />
              : <XCircle className="h-7 w-7 text-red-400" />
            }
          </div>
          <div className="flex-1">
            <p className={`text-xl font-extrabold ${approved ? "text-emerald-400" : "text-red-400"}`}>
              {approved ? "Likely Approved" : "Likely Rejected"}
            </p>
            <p className="mt-0.5 text-sm text-slate-400">
              The model is <span className="font-semibold text-slate-300">{pct}%</span> confident in this decision.
            </p>
          </div>
          <Badge label={result.risk_level + " Risk"} variant={riskBadge[result.risk_level]} />
        </div>
      </div>

      {/* Key numbers */}
      <div className="mb-5 grid grid-cols-2 gap-4">
        <Card accent={approved ? "green" : "red"}>
          <div className="flex items-center gap-3 mb-4">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 ring-1 ring-blue-500/20">
              <TrendingUp className="h-4 w-4 text-blue-400" />
            </div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Approval Probability</p>
          </div>
          <p className="text-4xl font-extrabold text-white tracking-tight">
            {formatPercent(result.approval_probability)}
          </p>
          <div className="mt-4 h-1.5 w-full rounded-full bg-slate-800">
            <div
              className={`h-1.5 rounded-full transition-all duration-1000 ${approved ? "bg-gradient-to-r from-emerald-500 to-teal-400" : "bg-gradient-to-r from-red-500 to-rose-400"}`}
              style={{ width: `${pct}%` }}
            />
          </div>
        </Card>

        <Card accent={approved ? "green" : "none"}>
          <div className="flex items-center gap-3 mb-4">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 ring-1 ring-emerald-500/20">
              <Banknote className="h-4 w-4 text-emerald-400" />
            </div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Max Eligible</p>
          </div>
          <p className="text-4xl font-extrabold text-white tracking-tight">
            {formatCurrency(result.max_loan_amount)}
          </p>
          <p className="mt-4 text-xs text-slate-600">Recommended maximum by the model</p>
        </Card>
      </div>

      {/* Decision factors */}
      <Card title="Decision Factors" accent="blue" className="mb-5">
        <p className="mb-4 text-xs text-slate-600">
          These factors had the most influence on this decision:
        </p>
        <ul className="flex flex-col gap-2">
          {Object.entries(result.factors).map(([key, value]) => {
            const isPositive = /positive|healthy|good|low risk|no defaults|collateral/i.test(value);
            const isNegative = /negative|too high|poor|high risk/i.test(value);
            return (
              <li
                key={key}
                className="flex items-start gap-3 rounded-xl border border-slate-800/60 bg-slate-900/40 px-4 py-3 transition-colors hover:bg-slate-900/70"
              >
                <div className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md ${
                  isNegative ? "bg-red-500/10" : isPositive ? "bg-emerald-500/10" : "bg-amber-500/10"
                }`}>
                  {isNegative
                    ? <XCircle className="h-3 w-3 text-red-400" />
                    : isPositive
                    ? <CheckCircle className="h-3 w-3 text-emerald-400" />
                    : <AlertTriangle className="h-3 w-3 text-amber-400" />
                  }
                </div>
                <div>
                  <span className="text-xs font-semibold text-slate-300 capitalize">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="ml-2 text-xs text-slate-500">{value}</span>
                </div>
              </li>
            );
          })}
        </ul>
      </Card>

      {/* Disclaimer */}
      <div className="mb-7 flex items-start gap-3 rounded-xl border border-amber-500/15 bg-amber-500/5 px-4 py-3">
        <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-500/70" />
        <p className="text-xs text-amber-600/80 leading-relaxed">
          <span className="font-semibold text-amber-500/90">Disclaimer:</span> This is an AI-generated estimate for informational purposes only.
          Final loan decisions are made by human underwriters and may differ from this prediction.
        </p>
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
