import { Users, TrendingUp, Target, Calendar, UserCheck, UserX } from 'lucide-react';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { useLanguage } from '@/contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { patientService, type Patient } from '@/services/patients';
import { apiService, User } from '@/services/api';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

export default function Dashboard() {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingUsers, setLoadingUsers] = useState(false);

  useEffect(() => {
    loadPatients();
    if (user?.role === 'admin') {
      loadUsers();
    }
  }, [user]);

  const loadPatients = async () => {
    try {
      setLoading(true);
      const data = await patientService.getPatients();
      setPatients(data);
    } catch (error) {
      console.error('Error loading patients:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    setLoadingUsers(true);
    try {
      const fetchedUsers = await apiService.getUsers();
      setUsers(fetchedUsers);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 
        (language === 'es' ? 'Error al cargar usuarios' : 'Error loading users'));
    } finally {
      setLoadingUsers(false);
    }
  };

  // Calcular métricas reales
  const totalPatients = patients.length;
  
  const patientsWithPredictions = patients.filter(p => p.prediction_profile !== null);
  
  // Predicciones de hoy (filtrar por última actualización - simplificado)
  const today = new Date().toISOString().split('T')[0];
  const predictionsToday = patientsWithPredictions.length; // Simplificado - necesitaría fecha de predicción

  // Calcular tasa de éxito como porcentaje de predicciones hoy / total de pacientes
  const successRate = totalPatients > 0
    ? ((predictionsToday / totalPatients) * 100).toFixed(2)
    : '0.00';

  // Últimos 5 pacientes
  const recentPatients = [...patients].reverse().slice(0, 5);

  // Historial de predicciones (pacientes con predicción)
  const predictionHistory = patientsWithPredictions.reverse().slice(0, 10);

  // User metrics (admin only)
  const totalUsers = users.length;
  const activeUsers = users.filter(u => u.is_active).length;
  const inactiveUsers = users.filter(u => !u.is_active).length;
  const adminUsers = users.filter(u => u.role === 'admin').length;
  const doctorUsers = users.filter(u => u.role === 'médico').length;

  // Data for pie charts (admin only)
  const roleDistributionData = [
    { name: language === 'es' ? 'Administradores' : 'Administrators', value: adminUsers, color: 'hsl(var(--primary))' },
    { name: language === 'es' ? 'Médicos' : 'Doctors', value: doctorUsers, color: 'hsl(var(--chart-2))' }
  ];

  const statusDistributionData = [
    { name: language === 'es' ? 'Activos' : 'Active', value: activeUsers, color: 'hsl(var(--success))' },
    { name: language === 'es' ? 'Inactivos' : 'Inactive', value: inactiveUsers, color: 'hsl(var(--destructive))' }
  ];

  const metrics = user?.role === 'admin' ? [
    {
      title: language === 'es' ? 'Total Usuarios' : 'Total Users',
      value: totalUsers.toString(),
      icon: Users,
    },
    {
      title: language === 'es' ? 'Usuarios Activos' : 'Active Users',
      value: activeUsers.toString(),
      icon: UserCheck,
    },
    {
      title: language === 'es' ? 'Usuarios Inactivos' : 'Inactive Users',
      value: inactiveUsers.toString(),
      icon: UserX,
    },
  ] : [
    {
      title: t('totalPatients'),
      value: totalPatients.toString(),
      icon: Users,
    },
    {
      title: t('predictionsToday'),
      value: predictionsToday.toString(),
      icon: TrendingUp,
    },
    {
      title: t('successRate'),
      value: `${successRate}%`,
      icon: Target,
    },
  ];

  const getProfileColor = (profile: number | null): string => {
    if (!profile) return 'bg-muted';
    if (profile <= 3) return 'bg-green-500';
    if (profile <= 6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          {user?.role === 'admin' 
            ? (language === 'es' ? 'Panel de Administración' : 'Admin Panel')
            : t('dashboard')}
        </h1>
        <p className="text-muted-foreground mt-2">
          {user?.role === 'admin'
            ? (language === 'es' ? 'Gestione usuarios y visualice métricas del sistema' : 'Manage users and view system metrics')
            : 'Monitor your disability assessment activities'}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {metrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {user?.role === 'admin' && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>
                {language === 'es' ? 'Distribución por Rol' : 'Role Distribution'}
              </CardTitle>
              <CardDescription>
                {language === 'es' 
                  ? 'Usuarios organizados por tipo de rol' 
                  : 'Users organized by role type'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {totalUsers > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={roleDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {roleDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[250px] text-muted-foreground">
                  {language === 'es' ? 'No hay datos disponibles' : 'No data available'}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>
                {language === 'es' ? 'Estado de Usuarios' : 'User Status'}
              </CardTitle>
              <CardDescription>
                {language === 'es' 
                  ? 'Usuarios activos vs inactivos' 
                  : 'Active vs inactive users'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {totalUsers > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={statusDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {statusDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[250px] text-muted-foreground">
                  {language === 'es' ? 'No hay datos disponibles' : 'No data available'}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {user?.role !== 'admin' && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>{t('recentPatients')}</CardTitle>
            <Button variant="ghost" size="sm" onClick={() => navigate('/patients')}>
              {t('viewAll')}
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentPatients.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">
                  {t('noPatientsYet')}
                </p>
              ) : (
                recentPatients.map((patient) => (
                  <div 
                    key={patient.id}
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors cursor-pointer"
                    onClick={() => navigate('/patients')}
                  >
                    <div className="flex-1">
                      <p className="font-medium">{patient.nombre_apellidos}</p>
                      <p className="text-sm text-muted-foreground">
                        {patient.edad} años - {patient.genero}
                      </p>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4 inline mr-1" />
                      {new Date(patient.fecha_nacimiento).toLocaleDateString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>{t('predictionHistory')}</CardTitle>
            <Button variant="ghost" size="sm" onClick={() => navigate('/predictions')}>
              {t('viewAll')}
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {predictionHistory.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">
                  {t('addFirstPatient')}
                </p>
              ) : (
                predictionHistory.map((patient) => (
                  <div 
                    key={patient.id}
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors cursor-pointer"
                    onClick={() => navigate('/predictions')}
                  >
                    <div className="flex-1">
                      <p className="font-medium">{patient.nombre_apellidos}</p>
                      <p className="text-sm text-muted-foreground line-clamp-1">
                        {patient.prediction_description || 'Sin descripción'}
                      </p>
                    </div>
                    <Badge 
                      className={`${getProfileColor(patient.prediction_profile)} text-white`}
                    >
                      Perfil {patient.prediction_profile}
                    </Badge>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
        </div>
      )}
    </div>
  );
}
