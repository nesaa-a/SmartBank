import { type InputHTMLAttributes, forwardRef } from "react";
import { clsx } from "clsx";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, className, ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-xs font-semibold tracking-wide text-slate-400 uppercase">
          {label}
          {props.required && <span className="ml-1 text-blue-400">*</span>}
        </label>
      )}
      <input
        ref={ref}
        className={clsx(
          "w-full rounded-xl border bg-slate-900/60 px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 transition-all duration-200",
          "focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/60 focus:bg-slate-900",
          "hover:border-slate-600",
          error
            ? "border-red-500/60 bg-red-950/20 focus:ring-red-500/40 focus:border-red-500/60"
            : "border-slate-700/60",
          className
        )}
        {...props}
      />
      {hint && !error && <p className="text-xs text-slate-600">{hint}</p>}
      {error && <p className="text-xs text-red-400">{error}</p>}
    </div>
  )
);
Input.displayName = "Input";
