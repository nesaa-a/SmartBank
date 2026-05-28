import { LogOut, User, Bell, ChevronDown } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="relative flex h-16 shrink-0 items-center justify-between border-b border-slate-800/80 bg-slate-950/90 px-6 backdrop-blur-xl">
      {/* Subtle top glow line */}
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-blue-500/30 to-transparent" />

      {/* Brand */}
      <div className="flex items-center gap-3">
        <div className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg shadow-blue-900/50">
          <span className="text-sm font-black text-white tracking-tight">S</span>
          <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent" />
        </div>
        <div className="flex flex-col leading-none">
          <span className="text-sm font-bold text-white tracking-tight">SmartBank</span>
          <span className="text-[10px] font-medium text-slate-500 tracking-widest uppercase">AI Platform</span>
        </div>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-2">
        <button className="relative flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-800/80 hover:text-slate-300 transition-all duration-200">
          <Bell className="h-4 w-4" />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-blue-500" />
        </button>

        <div className="mx-1 h-5 w-px bg-slate-800" />

        <div className="flex items-center gap-2.5 rounded-xl border border-slate-800/80 bg-slate-900/60 px-3 py-1.5 backdrop-blur-sm">
          <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500/20 to-indigo-500/20 ring-1 ring-blue-500/30">
            <User className="h-3 w-3 text-blue-400" />
          </div>
          <div className="flex flex-col leading-none">
            <span className="text-xs font-semibold text-slate-200">{user?.full_name ?? "User"}</span>
            <span className="text-[10px] text-slate-500 truncate max-w-[120px]">{user?.email ?? ""}</span>
          </div>
          <ChevronDown className="h-3 w-3 text-slate-600" />
        </div>

        <button
          onClick={logout}
          title="Sign out"
          className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 hover:bg-red-500/10 hover:text-red-400 border border-transparent hover:border-red-500/20 transition-all duration-200"
        >
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}
