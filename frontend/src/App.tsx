import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LoanApplicationPage } from "./pages/LoanApplicationPage";
import { LoanResultPage } from "./pages/LoanResultPage";
import { ApplicationsHistoryPage } from "./pages/ApplicationsHistoryPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes — Layout handles auth redirect */}
        <Route path="/dashboard" element={<Layout><DashboardPage /></Layout>} />
        <Route path="/apply" element={<Layout><LoanApplicationPage /></Layout>} />
        <Route path="/result" element={<Layout><LoanResultPage /></Layout>} />
        <Route path="/applications" element={<Layout><ApplicationsHistoryPage /></Layout>} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
