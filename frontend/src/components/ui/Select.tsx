import { type SelectHTMLAttributes, forwardRef } from "react";
import { clsx } from "clsx";

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { value: string; label: string }[];
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, options, className, ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-xs font-semibold tracking-wide text-slate-400 uppercase">
          {label}
          {props.required && <span className="ml-1 text-blue-400">*</span>}
        </label>
      )}
      <select
        ref={ref}
        className={clsx(
          "w-full rounded-xl border bg-slate-900/60 px-4 py-2.5 text-sm text-slate-100 transition-all duration-200",
          "focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/60 focus:bg-slate-900",
          "hover:border-slate-600",
          error ? "border-red-500/60" : "border-slate-700/60",
          className
        )}
        {...props}
      >
        <option value="" className="bg-slate-900 text-slate-400">— Select —</option>
        {options.map((o) => (
          <option key={o.value} value={o.value} className="bg-slate-900 text-slate-100">
            {o.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-red-400">{error}</p>}
    </div>
  )
);
Select.displayName = "Select";
