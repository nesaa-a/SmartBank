import { useNavigate } from "react-router-dom";
import { FileText, TrendingUp, ShieldCheck, ArrowRight, CircleDot, Cpu, BarChart3 } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";

const stats = [
  {
    label: "AI Model Accuracy",
    value: "87.8%",
    icon: TrendingUp,
    gradient: "from-emerald-500/20 to-teal-500/10",
    iconColor: "text-emerald-400",
    ring: "ring-emerald-500/20",
    accent: "green" as const,
    delta: "+2.1% vs baseline",
  },
  {
    label: "Applications Processed",
    value: "6,000+",
    icon: FileText,
    gradient: "from-blue-500/20 to-indigo-500/10",
    iconColor: "text-blue-400",
    ring: "ring-blue-500/20",
    accent: "blue" as const,
    delta: "Real-world dataset",
  },
  {
    label: "Approval Rate",
    value: "~51%",
    icon: ShieldCheck,
    gradient: "from-violet-500/20 to-purple-500/10",
    iconColor: "text-violet-400",
    ring: "ring-violet-500/20",
    accent: "purple" as const,
    delta: "Based on model output",
  },
];

const steps = [
  {
    num: "01",
    icon: FileText,
    title: "Fill in the form",
    desc: "Enter your personal and financial details in our secure application form.",
  },
  {
    num: "02",
    icon: Cpu,
    title: "AI Analysis",
    desc: "Our XGBoost model analyses 14 financial factors to compute your risk profile.",
  },
  {
    num: "03",
    icon: BarChart3,
    title: "Instant Result",
    desc: "Get an approval decision, confidence score, and maximum eligible loan amount.",
  },
];

export function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();
  const firstName = user?.full_name?.split(" ")[0] ?? "there";

  return (
    <div className="flex flex-col gap-8">
      {/* Hero greeting */}
      <div className="relative overflow-hidden rounded-2xl border border-slate-800/80 bg-gradient-to-br from-slate-900 to-slate-950 p-7 shadow-xl">
        <div className="pointer-events-none absolute right-0 top-0 h-full w-1/2 bg-gradient-to-l from-blue-600/5 to-transparent" />
        <div className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-blue-600/10 blur-2xl" />

        <div className="relative">
          <div className="flex items-center gap-2 mb-3">
            <CircleDot className="h-3 w-3 text-emerald-400 animate-pulse" />
            <span className="text-xs font-medium text-emerald-400 tracking-wide">System online</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white">
            Good day, <span className="text-gradient">{firstName}</span> 👋
          </h1>
          <p className="mt-2 text-sm text-slate-400 max-w-lg">
            Welcome to SmartBank — get AI-powered loan decisions in seconds. No waiting, no guesswork.
          </p>
          <div className="mt-5 flex gap-3">
            <Button onClick={() => navigate("/apply")} size="lg">
              Apply for a Loan
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button variant="secondary" onClick={() => navigate("/applications")}>
              View History
            </Button>
          </div>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {stats.map(({ label, value, icon: Icon, gradient, iconColor, ring, accent, delta }) => (
          <Card key={label} accent={accent} className="overflow-hidden">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-3xl font-extrabold text-white tracking-tight">{value}</p>
                <p className="mt-1 text-sm font-medium text-slate-400">{label}</p>
                <p className="mt-2 text-xs text-slate-600">{delta}</p>
              </div>
              <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${gradient} ring-1 ${ring}`}>
                <Icon className={`h-5 w-5 ${iconColor}`} />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* How it works */}
      <Card title="How it works" accent="blue">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          {steps.map(({ num, icon: Icon, title, desc }) => (
            <div key={num} className="flex flex-col gap-3">
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 ring-1 ring-blue-500/20">
                  <Icon className="h-4 w-4 text-blue-400" />
                </div>
                <span className="text-xs font-black text-slate-700 tracking-widest">{num}</span>
              </div>
              <div>
                <p className="font-semibold text-slate-200 text-sm">{title}</p>
                <p className="mt-1 text-xs text-slate-500 leading-relaxed">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
