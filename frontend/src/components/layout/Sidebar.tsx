import { NavLink } from "react-router-dom";
import { LayoutDashboard, FileText, ClipboardList, ShieldCheck } from "lucide-react";
import { clsx } from "clsx";
import { useAuthStore } from "../../store/authStore";

const nav = [
  { to: "/dashboard",    label: "Dashboard",     icon: LayoutDashboard },
  { to: "/apply",        label: "Apply for Loan", icon: FileText },
  { to: "/applications", label: "My Applications", icon: ClipboardList },
];

const adminNav = [
  { to: "/admin", label: "Admin Panel", icon: ShieldCheck },
];

export function Sidebar() {
  const user = useAuthStore((s) => s.user);

  return (
    <aside className="flex w-60 flex-col border-r border-gray-200 bg-gray-50 py-6">
      <nav className="flex flex-col gap-1 px-3">
        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-100 text-blue-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}

        {user?.is_superuser && (
          <>
            <div className="my-2 border-t border-gray-200" />
            {adminNav.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  clsx(
                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-blue-100 text-blue-700"
                      : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </>
        )}
      </nav>
    </aside>
  );
}
