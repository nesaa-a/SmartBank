import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { ShieldCheck, Zap, TrendingUp } from "lucide-react";
import { authService } from "../services/authService";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";

const schema = z.object({
  full_name: z.string().min(2, "Full name must be at least 2 characters"),
  username: z.string().min(3, "Username must be at least 3 characters").regex(/^\w+$/, "Only letters, numbers, underscores"),
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});
type FormData = z.infer<typeof schema>;

const features = [
  { icon: Zap,         text: "Instant AI decisions" },
  { icon: ShieldCheck, text: "Bank-grade security" },
  { icon: TrendingUp,  text: "87.8% model accuracy" },
];

export function RegisterPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: FormData) {
    setError("");
    try {
      await authService.register(data);
      navigate("/login", { state: { registered: true } });
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(msg ?? "Registration failed. Please try again.");
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-950 bg-grid">
      {/* Ambient glows */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -top-60 -left-40 h-[500px] w-[500px] rounded-full bg-blue-600/8 blur-[100px] animate-glow-pulse" />
        <div className="absolute -bottom-40 -right-40 h-[400px] w-[400px] rounded-full bg-indigo-600/8 blur-[100px] animate-glow-pulse" style={{ animationDelay: "1s" }} />
      </div>

      {/* Left panel */}
      <div className="hidden lg:flex lg:w-[45%] flex-col justify-between border-r border-slate-800/60 bg-slate-900/30 px-12 py-12 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg shadow-blue-900/50">
            <span className="text-base font-black text-white">S</span>
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent" />
          </div>
          <span className="text-lg font-bold text-white tracking-tight">SmartBank</span>
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="text-4xl font-extrabold leading-tight text-white">
              Start your journey<br />
              <span className="text-gradient">to smarter loans.</span>
            </h1>
            <p className="mt-4 text-base text-slate-400 leading-relaxed max-w-sm">
              Create your free account and get AI-powered loan assessments in seconds — no paperwork needed.
            </p>
          </div>
          <ul className="space-y-3">
            {features.map(({ icon: Icon, text }) => (
              <li key={text} className="flex items-center gap-3 text-sm text-slate-400">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 ring-1 ring-blue-500/20">
                  <Icon className="h-3.5 w-3.5 text-blue-400" />
                </div>
                {text}
              </li>
            ))}
          </ul>
        </div>

        <p className="text-xs text-slate-700">© 2025 SmartBank. All rights reserved.</p>
      </div>

      {/* Right panel — form */}
      <div className="relative flex flex-1 items-center justify-center px-6 py-12">
        <div className="w-full max-w-sm animate-scale-in">
          {/* Mobile logo */}
          <div className="mb-8 flex flex-col items-center lg:hidden">
            <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-xl shadow-blue-900/50 mb-4">
              <span className="text-2xl font-black text-white">S</span>
            </div>
            <h1 className="text-xl font-bold text-white">SmartBank</h1>
          </div>

          <div className="mb-7">
            <h2 className="text-2xl font-bold text-white">Create your account</h2>
            <p className="mt-1 text-sm text-slate-500">Free forever — no credit card required</p>
          </div>

          <div className="rounded-2xl border border-slate-800/80 bg-slate-900/70 p-7 shadow-2xl shadow-black/50 backdrop-blur-sm">
            <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
              <Input
                label="Full name"
                placeholder="Jane Doe"
                error={errors.full_name?.message}
                required
                {...register("full_name")}
              />
              <Input
                label="Username"
                placeholder="janedoe"
                error={errors.username?.message}
                required
                {...register("username")}
              />
              <Input
                label="Email address"
                type="email"
                placeholder="you@example.com"
                error={errors.email?.message}
                required
                {...register("email")}
              />
              <Input
                label="Password"
                type="password"
                placeholder="••••••••"
                hint="At least 8 characters"
                error={errors.password?.message}
                required
                {...register("password")}
              />

              {error && (
                <div className="rounded-xl border border-red-500/20 bg-red-500/8 px-4 py-3 text-sm text-red-400">
                  {error}
                </div>
              )}

              <Button type="submit" size="lg" loading={isSubmitting} className="mt-1 w-full">
                {isSubmitting ? "Creating account…" : "Create account"}
              </Button>
            </form>

            <p className="mt-5 text-center text-sm text-slate-500">
              Already have an account?{" "}
              <Link to="/login" className="font-semibold text-blue-400 hover:text-blue-300 transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
