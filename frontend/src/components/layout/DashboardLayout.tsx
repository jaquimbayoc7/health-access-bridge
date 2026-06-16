import { Navigate, Outlet, useLocation, Link } from 'react-router-dom';
import { SidebarProvider } from '@/components/ui/sidebar';
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { AppSidebar } from './AppSidebar';
import { Header } from './Header';
import { useAuth } from '@/contexts/AuthContext';

const ROUTE_LABELS: Record<string, string> = {
  '/dashboard': 'Panel',
  '/patients': 'Pacientes',
  '/predictions': 'Predicciones',
  '/analytics': 'Análisis',
  '/predictive-guide': 'Guía Predictiva',
  '/help': 'Ayuda',
  '/settings': 'Configuración',
  '/admin': 'Administración',
};

function DynamicBreadcrumb() {
  const location = useLocation();
  const label = ROUTE_LABELS[location.pathname];
  if (!label) return null;
  return (
    <Breadcrumb className="px-6 pt-4 pb-0">
      <BreadcrumbList>
        <BreadcrumbItem>
          <BreadcrumbLink asChild>
            <Link to="/dashboard">Inicio</Link>
          </BreadcrumbLink>
        </BreadcrumbItem>
        {location.pathname !== '/dashboard' && (
          <>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>{label}</BreadcrumbPage>
            </BreadcrumbItem>
          </>
        )}
      </BreadcrumbList>
    </Breadcrumb>
  );
}

export function DashboardLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <DynamicBreadcrumb />
          <main className="flex-1 overflow-y-auto p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
