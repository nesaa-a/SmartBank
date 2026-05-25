import { useNavigate } from "react-router-dom";
import { FileText, TrendingUp, ShieldCheck, ArrowRight } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";

const stats = [
  { label: "AI Model Accuracy", value: "87.8%", icon: TrendingUp, color: "text-green-600 bg-green-50" },
  { label: "Applications Processed", value: "6,000+", icon: FileText, color: "text-blue-600 bg-blue-50" },
  { label: "Approval Rate", value: "~51%", icon: ShieldCheck, color: "text-purple-600 bg-purple-50" },
];

export function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();

  return (
    <div className="flex flex-col gap-8">
      {/* Greeting */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Good day, {user?.full_name?.split(" ")[0] ?? "there"}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome to SmartBank — AI-powered loan decisions in seconds.
        </p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {stats.map(({ label, value, icon: Icon, color }) => (
          <Card key={label} className="flex items-center gap-4">
            <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${color}`}>
              <Icon className="h-6 w-6" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{value}</p>
              <p className="text-sm text-gray-500">{label}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* CTA card */}
      <Card title="Apply for a Loan">
        <p className="mb-6 text-sm text-gray-600 max-w-xl">
          Our AI model analyses your financial profile and returns an instant decision —
          including whether your application is likely to be approved and the maximum
          loan amount you may qualify for.
        </p>
        <div className="flex gap-3">
          <Button onClick={() => navigate("/apply")} size="lg">
            Start Application
            <ArrowRight className="h-4 w-4" />
          </Button>
          <Button variant="secondary" onClick={() => navigate("/applications")}>
            View Past Applications
          </Button>
        </div>
      </Card>

      {/* How it works */}
      <Card title="How it works">
        <ol className="flex flex-col gap-4 sm:flex-row sm:gap-8">
          {[
            ["1. Fill in the form", "Enter your personal and financial information in our secure application form."],
            ["2. AI Analysis", "Our XGBoost model analyses 14 financial factors to compute your risk profile."],
            ["3. Instant Result", "Receive an approval decision, confidence score, and maximum eligible loan amount."],
          ].map(([title, desc]) => (
            <li key={title} className="flex flex-1 flex-col gap-1">
              <p className="font-semibold text-gray-800">{title}</p>
              <p className="text-sm text-gray-500">{desc}</p>
            </li>
          ))}
        </ol>
      </Card>
    </div>
  );
}
