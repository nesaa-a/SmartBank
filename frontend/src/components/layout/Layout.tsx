import { type ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { useAuthStore } from "../../store/authStore";

export function Layout({ children }: { children: ReactNode }) {
  const isAuthenticated = useAuthStore((s) => !!s.accessToken);

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return (
    <div className="flex h-screen flex-col bg-gray-100">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8">{children}</main>
      </div>
    </div>
  );
}
