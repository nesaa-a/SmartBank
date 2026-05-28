import { NavLink } from "react-router-dom";
import { LayoutDashboard, FileText, ClipboardList, ShieldCheck, Sparkles } from "lucide-react";
import { clsx } from "clsx";
import { useAuthStore } from "../../store/authStore";

const nav = [
  { to: "/dashboard",    label: "Dashboard",       icon: LayoutDashboard },
  { to: "/apply",        label: "Apply for Loan",   icon: FileText },
  { to: "/applications", label: "My Applications",  icon: ClipboardList },
];

const adminNav = [
  { to: "/admin", label: "Admin Panel", icon: ShieldCheck },
];

export function Sidebar() {
  const user = useAuthStore((s) => s.user);

  return (
    <aside className="flex w-60 shrink-0 flex-col border-r border-slate-800/80 bg-slate-950 overflow-y-auto">
      {/* Section label */}
      <div className="px-4 pt-6 pb-1">
        <p className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-600">
          Menu
        </p>
      </div>

      <nav className="flex flex-col gap-0.5 px-2 pb-4">
        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              clsx(
                "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-blue-500/10 text-blue-400"
                  : "text-slate-500 hover:bg-slate-800/60 hover:text-slate-300"
              )
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-r-full bg-gradient-to-b from-blue-400 to-indigo-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]" />
                )}
                <div className={clsx(
                  "flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-all duration-200",
                  isActive
                    ? "bg-blue-500/15 text-blue-400 shadow-sm shadow-blue-900/20"
                    : "text-slate-600 group-hover:text-slate-400"
                )}>
                  <Icon className="h-4 w-4" />
                </div>
                <span>{label}</span>
                {isActive && (
                  <span className="ml-auto h-1.5 w-1.5 rounded-full bg-blue-500 shadow-[0_0_6px_rgba(59,130,246,0.8)]" />
                )}
              </>
            )}
          </NavLink>
        ))}

        {user?.is_superuser && (
          <>
            <div className="my-3 mx-2 border-t border-slate-800/80" />
            <p className="px-3 pb-1 text-[10px] font-bold uppercase tracking-[0.15em] text-slate-600">
              Admin
            </p>
            {adminNav.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  clsx(
                    "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-violet-500/10 text-violet-400"
                      : "text-slate-500 hover:bg-slate-800/60 hover:text-slate-300"
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-r-full bg-gradient-to-b from-violet-400 to-purple-500 shadow-[0_0_8px_rgba(139,92,246,0.8)]" />
                    )}
                    <div className={clsx(
                      "flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition-all duration-200",
                      isActive
                        ? "bg-violet-500/15 text-violet-400"
                        : "text-slate-600 group-hover:text-slate-400"
                    )}>
                      <Icon className="h-4 w-4" />
                    </div>
                    <span>{label}</span>
                  </>
                )}
              </NavLink>
            ))}
          </>
        )}
      </nav>

      {/* Footer branding */}
      <div className="mt-auto border-t border-slate-800/80 px-4 py-4">
        <div className="flex items-center gap-2 text-slate-600">
          <Sparkles className="h-3.5 w-3.5 text-blue-500/60" />
          <span className="text-[10px] font-medium tracking-wide">Powered by XGBoost AI</span>
        </div>
      </div>
    </aside>
  );
}
