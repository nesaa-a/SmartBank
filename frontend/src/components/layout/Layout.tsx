import { type ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { useAuthStore } from "../../store/authStore";

export function Layout({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore((s) => !!s.accessToken);

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return (
    <div className="flex h-full min-h-screen flex-col bg-slate-950 bg-grid">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto px-8 py-7">
          <div className="animate-fade-in mx-auto max-w-5xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
