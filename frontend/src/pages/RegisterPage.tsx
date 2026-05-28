import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { authService } from "../services/authService";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";

const schema = z.object({
  full_name: z.string().min(2, "Full name must be at least 2 characters"),
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .regex(/^\w+$/, "Only letters, numbers, underscores"),
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormData = z.infer<typeof schema>;

export function RegisterPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: FormData) {
    setError("");

    try {
      await authService.register(data);
      navigate("/login", { state: { registered: true } });
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail;

      setError(msg ?? "Registration failed. Please try again.");
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 flex items-center justify-center px-5 py-12">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(37,99,235,0.35),transparent_32%),radial-gradient(circle_at_80%_90%,rgba(34,197,94,0.18),transparent_35%)]" />

      <div className="absolute top-24 left-20 h-72 w-72 rounded-full bg-blue-600/10 blur-3xl" />
      <div className="absolute bottom-20 right-20 h-72 w-72 rounded-full bg-emerald-500/10 blur-3xl" />

      <div className="relative w-full max-w-[580px]">
        <div className="mb-8 flex justify-center">
          <div className="flex items-center gap-4">
            <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center shadow-xl shadow-blue-500/25">
              <span className="text-white font-bold text-2xl">S</span>
            </div>

            <div>
              <h2 className="text-white font-semibold text-2xl leading-none">
                SmartBank
              </h2>
              <p className="text-slate-500 text-sm mt-1">
                Your financial assistant
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-[34px] border border-white/10 bg-white/[0.055] backdrop-blur-xl shadow-2xl shadow-black/40 px-8 py-9 sm:px-11 sm:py-10">
          <div className="mb-8 text-center">
            <p className="inline-flex items-center rounded-full border border-blue-400/20 bg-blue-500/10 px-4 py-1.5 text-xs font-medium text-blue-300 mb-5">
              Free account
            </p>

            <h1 className="text-3xl font-semibold tracking-tight text-white">
              Create your account
            </h1>

            <p className="text-base text-slate-400 mt-3">
              Join SmartBank and start managing your finances smarter.
            </p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              label="Full name"
              placeholder="Jane Doe"
              error={errors.full_name?.message}
              className="h-14 rounded-2xl px-5 text-base"
              {...register("full_name")}
            />

            <Input
              label="Username"
              placeholder="janedoe"
              error={errors.username?.message}
              className="h-14 rounded-2xl px-5 text-base"
              {...register("username")}
            />

            <Input
              label="Email address"
              type="email"
              placeholder="you@example.com"
              error={errors.email?.message}
              className="h-14 rounded-2xl px-5 text-base"
              {...register("email")}
            />

            <Input
              label="Password"
              type="password"
              placeholder="At least 8 characters"
              error={errors.password?.message}
              className="h-14 rounded-2xl px-5 text-base"
              {...register("password")}
            />

            {error && (
              <div className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3.5">
                <p className="text-sm text-red-300">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              variant="solid"
              size="lg"
              loading={isSubmitting}
              className="w-full h-14 mt-2 rounded-2xl text-base font-semibold shadow-lg shadow-blue-500/20"
            >
              {isSubmitting ? "Creating account…" : "Create account"}
            </Button>
          </form>

          <div className="my-8 flex items-center gap-4">
            <div className="h-px flex-1 bg-white/10" />
            <span className="text-sm text-slate-500">or</span>
            <div className="h-px flex-1 bg-white/10" />
          </div>

          <p className="text-center text-base text-slate-400">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-semibold text-blue-400 hover:text-blue-300 transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>

        <p className="mt-6 text-center text-sm text-slate-600">
          No credit card required
        </p>
      </div>
    </div>
  );
}