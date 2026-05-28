import { type ReactNode } from "react";
import { clsx } from "clsx";

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  accent?: "blue" | "green" | "red" | "purple" | "none";
}

const accentBorder: Record<string, string> = {
  blue:   "border-t-blue-500/60",
  green:  "border-t-emerald-500/60",
  red:    "border-t-red-500/60",
  purple: "border-t-violet-500/60",
  none:   "border-t-transparent",
};

export function Card({ children, className, title, accent = "none" }: CardProps) {
  return (
    <div
      className={clsx(
        "rounded-2xl border border-slate-800/80 bg-slate-900/60 shadow-xl shadow-black/30 backdrop-blur-sm",
        "border-t-2",
        accentBorder[accent],
        className
      )}
    >
      {title && (
        <div className="flex items-center gap-3 border-b border-slate-800/80 px-6 py-4">
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide">{title}</h3>
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
}
