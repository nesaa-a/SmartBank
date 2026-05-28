import { clsx } from "clsx";

type BadgeVariant = "green" | "red" | "yellow" | "blue" | "gray" | "purple";

const styles: Record<BadgeVariant, string> = {
  green:  "bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 shadow-sm shadow-emerald-900/20",
  red:    "bg-red-500/10    text-red-400    border border-red-500/25    shadow-sm shadow-red-900/20",
  yellow: "bg-amber-500/10  text-amber-400  border border-amber-500/25  shadow-sm shadow-amber-900/20",
  blue:   "bg-blue-500/10   text-blue-400   border border-blue-500/25   shadow-sm shadow-blue-900/20",
  gray:   "bg-slate-700/40  text-slate-400  border border-slate-600/30",
  purple: "bg-violet-500/10 text-violet-400 border border-violet-500/25 shadow-sm shadow-violet-900/20",
};

export function Badge({ label, variant = "gray" }: { label: string; variant?: BadgeVariant }) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wide",
        styles[variant]
      )}
    >
      {label}
    </span>
  );
}
