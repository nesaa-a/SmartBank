import { useNavigate } from "react-router-dom";
import { FileText, Plus, CheckCircle, XCircle, TrendingUp, Banknote, Calendar } from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { formatCurrency, formatPercent } from "../utils/formatters";
import type { LoanPredictionResult } from "../types/loan";

interface StoredApplication {
  result: LoanPredictionResult;
  submittedAt: string;
  requestedAmount: number;
}

function loadHistory(): StoredApplication[] {
  try {
    return JSON.parse(localStorage.getItem("loan_history") ?? "[]");
  } catch {
    return [];
  }
}

export function ApplicationsHistoryPage() {
  const navigate = useNavigate();
  const history = loadHistory();

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-extrabold text-white">My Applications</h1>
          <p className="mt-1 text-sm text-slate-500">
            Your loan application history from this session.
          </p>
        </div>
        <Button onClick={() => navigate("/apply")}>
          <Plus className="h-4 w-4" />
          New Application
        </Button>
      </div>

      {history.length === 0 ? (
        <Card accent="blue">
          <div className="flex flex-col items-center gap-5 py-14 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-slate-700/50 bg-slate-800/50">
              <FileText className="h-7 w-7 text-slate-600" />
            </div>
            <div>
              <p className="font-semibold text-slate-300 text-base">No applications yet</p>
              <p className="mt-1.5 text-sm text-slate-600 max-w-xs">
                Submit your first loan application to see your history here.
              </p>
            </div>
            <Button onClick={() => navigate("/apply")}>
              Apply now
              <Plus className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      ) : (
        <div className="flex flex-col gap-3">
          {history.map((app, i) => {
            const approved = app.result.loan_approved;
            const risk = app.result.risk_level;
            return (
              <div
                key={i}
                className={`group relative overflow-hidden rounded-2xl border bg-slate-900/60 backdrop-blur-sm transition-all duration-200 hover:bg-slate-900/80 ${
                  approved
                    ? "border-slate-800/80 hover:border-emerald-500/20"
                    : "border-slate-800/80 hover:border-red-500/15"
                }`}
              >
                {/* Left accent bar */}
                <div className={`absolute left-0 top-0 h-full w-0.5 ${approved ? "bg-gradient-to-b from-emerald-500 to-teal-600" : "bg-gradient-to-b from-red-500 to-rose-600"}`} />

                <div className="px-5 py-4">
                  <div className="flex items-center gap-4">
                    {/* Icon */}
                    <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                      approved
                        ? "bg-emerald-500/10 ring-1 ring-emerald-500/20"
                        : "bg-red-500/10 ring-1 ring-red-500/20"
                    }`}>
                      {approved
                        ? <CheckCircle className="h-5 w-5 text-emerald-400" />
                        : <XCircle className="h-5 w-5 text-red-400" />
                      }
                    </div>

                    {/* Main info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`text-sm font-bold ${approved ? "text-emerald-400" : "text-red-400"}`}>
                          {approved ? "Likely Approved" : "Likely Rejected"}
                        </span>
                        <Badge
                          label={risk + " Risk"}
                          variant={risk === "Low" ? "green" : risk === "Medium" ? "yellow" : "red"}
                        />
                      </div>
                      <div className="mt-1 flex items-center gap-1.5 text-xs text-slate-600">
                        <Calendar className="h-3 w-3" />
                        {new Date(app.submittedAt).toLocaleDateString("en-GB", {
                          day: "numeric", month: "short", year: "numeric",
                        })}
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="hidden sm:flex items-center gap-6">
                      <div className="text-right">
                        <div className="flex items-center gap-1.5 justify-end text-slate-600 mb-0.5">
                          <Banknote className="h-3 w-3" />
                          <span className="text-[10px] font-medium uppercase tracking-wide">Requested</span>
                        </div>
                        <p className="text-sm font-bold text-slate-200">{formatCurrency(app.requestedAmount)}</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1.5 justify-end text-slate-600 mb-0.5">
                          <Banknote className="h-3 w-3" />
                          <span className="text-[10px] font-medium uppercase tracking-wide">Max eligible</span>
                        </div>
                        <p className="text-sm font-bold text-slate-200">{formatCurrency(app.result.max_loan_amount)}</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1.5 justify-end text-slate-600 mb-0.5">
                          <TrendingUp className="h-3 w-3" />
                          <span className="text-[10px] font-medium uppercase tracking-wide">Confidence</span>
                        </div>
                        <p className="text-sm font-bold text-slate-200">{formatPercent(app.result.approval_probability)}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
