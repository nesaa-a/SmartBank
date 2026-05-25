import { useNavigate } from "react-router-dom";
import { FileText, Plus } from "lucide-react";
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Applications</h1>
          <p className="mt-1 text-sm text-gray-500">
            Your loan application history from this session.
          </p>
        </div>
        <Button onClick={() => navigate("/apply")}>
          <Plus className="h-4 w-4" />
          New Application
        </Button>
      </div>

      {history.length === 0 ? (
        <Card>
          <div className="flex flex-col items-center gap-4 py-12 text-center">
            <FileText className="h-12 w-12 text-gray-300" />
            <div>
              <p className="font-medium text-gray-700">No applications yet</p>
              <p className="mt-1 text-sm text-gray-500">
                Submit your first loan application to see results here.
              </p>
            </div>
            <Button onClick={() => navigate("/apply")}>Apply now</Button>
          </div>
        </Card>
      ) : (
        <div className="flex flex-col gap-4">
          {history.map((app, i) => (
            <Card key={i}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-full text-white text-sm font-bold ${app.result.loan_approved ? "bg-green-500" : "bg-red-400"}`}>
                    {app.result.loan_approved ? "Y" : "N"}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      Requested: {formatCurrency(app.requestedAmount)}
                    </p>
                    <p className="text-sm text-gray-500">{new Date(app.submittedAt).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4 text-right">
                  <div>
                    <p className="text-xs text-gray-400">Max eligible</p>
                    <p className="font-semibold text-gray-800">{formatCurrency(app.result.max_loan_amount)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-400">Confidence</p>
                    <p className="font-semibold text-gray-800">{formatPercent(app.result.approval_probability)}</p>
                  </div>
                  <Badge
                    label={app.result.risk_level + " Risk"}
                    variant={app.result.risk_level === "Low" ? "green" : app.result.risk_level === "Medium" ? "yellow" : "red"}
                  />
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
