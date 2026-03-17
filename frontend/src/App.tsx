import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import LoginLanding from "./pages/LoginLanding";
import Dashboard from "./pages/Dashboard";
import Patients from "./pages/Patients";
import Predictions from "./pages/Predictions";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import AdminPanel from "./pages/AdminPanel";
import PredictiveGuide from "./pages/PredictiveGuide";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const AdminRoute = () => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== 'admin') return <Navigate to="/dashboard" replace />;
  return <Outlet />;
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <AuthProvider>
        <LanguageProvider>
          <TooltipProvider>
            <Toaster />
            <Sonner />
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/login" element={<LoginLanding />} />
              <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/patients" element={<Patients />} />
                <Route path="/predictions" element={<Predictions />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/predictive-guide" element={<PredictiveGuide />} />
                <Route path="/settings" element={<Settings />} />
                <Route element={<AdminRoute />}>
                  <Route path="/admin" element={<AdminPanel />} />
                </Route>
              </Route>
              <Route path="*" element={<NotFound />} />
            </Routes>
          </TooltipProvider>
        </LanguageProvider>
      </AuthProvider>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
