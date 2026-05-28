import { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { ShieldCheck, Zap, TrendingUp } from "lucide-react";
import { useAuth } from "../hooks/useAuth";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";

const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(1, "Password is required"),
});
type FormData = z.infer<typeof schema>;

const features = [
  { icon: Zap,        text: "Instant AI decisions" },
  { icon: ShieldCheck, text: "Bank-grade security" },
  { icon: TrendingUp, text: "87.8% model accuracy" },
];

export function LoginPage() {
  const { login } = useAuth();
  const [error, setError] = useState("");
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: FormData) {
    setError("");
    try {
      await login(data.email, data.password);
    } catch {
      setError("Invalid email or password. Please try again.");
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-950 bg-grid">
      {/* Ambient glows */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -top-60 -left-40 h-[500px] w-[500px] rounded-full bg-blue-600/8 blur-[100px] animate-glow-pulse" />
        <div className="absolute -bottom-40 -right-40 h-[400px] w-[400px] rounded-full bg-indigo-600/8 blur-[100px] animate-glow-pulse" style={{ animationDelay: "1s" }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[300px] w-[300px] rounded-full bg-violet-600/5 blur-[80px]" />
      </div>

      {/* Left panel — visible on lg+ */}
      <div className="hidden lg:flex lg:w-[45%] flex-col justify-between border-r border-slate-800/60 bg-slate-900/30 px-12 py-12 backdrop-blur-sm">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg shadow-blue-900/50">
            <span className="text-base font-black text-white">S</span>
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent" />
          </div>
          <span className="text-lg font-bold text-white tracking-tight">SmartBank</span>
        </div>

        {/* Hero text */}
        <div className="space-y-6">
          <div>
            <h1 className="text-4xl font-extrabold leading-tight text-white">
              Smarter lending,<br />
              <span className="text-gradient">powered by AI.</span>
            </h1>
            <p className="mt-4 text-base text-slate-400 leading-relaxed max-w-sm">
              Get instant, data-driven loan decisions. Our XGBoost model analyses your profile in seconds.
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
            <h2 className="text-2xl font-bold text-white">Welcome back</h2>
            <p className="mt-1 text-sm text-slate-500">Sign in to your account to continue</p>
          </div>

          <div className="rounded-2xl border border-slate-800/80 bg-slate-900/70 p-7 shadow-2xl shadow-black/50 backdrop-blur-sm">
            <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
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
                {isSubmitting ? "Signing in…" : "Sign in"}
              </Button>
            </form>

            <p className="mt-5 text-center text-sm text-slate-500">
              No account?{" "}
              <Link to="/register" className="font-semibold text-blue-400 hover:text-blue-300 transition-colors">
                Create one free
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
