import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useLanguage } from '@/contexts/LanguageContext';
import { useState, useEffect } from 'react';
import { patientService, type Patient } from '@/services/patients';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function Analytics() {
  const { t } = useLanguage();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPatients();
  }, []);

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

  // Filtrar pacientes con predicciones
  const patientsWithPredictions = patients.filter(p => p.prediction_profile !== null);

  // Datos para gráfica de distribución de perfiles (0, 1, 2)
  const profileDistribution = Array.from({ length: 3 }, (_, i) => {
    const profile = i; // 0, 1, 2
    const count = patientsWithPredictions.filter(p => p.prediction_profile === profile).length;
    return {
      perfil: `Perfil ${profile}`,
      cantidad: count,
    };
  }).filter(item => item.cantidad > 0);

  // Datos para gráfica de categorías físicas vs psicosociales
  const categoryData = [
    {
      name: 'Categoría Física',
      Leve: patientsWithPredictions.filter(p => p.cat_fisica === 'Leve').length,
      Moderada: patientsWithPredictions.filter(p => p.cat_fisica === 'Moderada').length,
      Grave: patientsWithPredictions.filter(p => p.cat_fisica === 'Grave').length,
      Completa: patientsWithPredictions.filter(p => p.cat_fisica === 'Completa').length,
    },
    {
      name: 'Categoría Psicosocial',
      Leve: patientsWithPredictions.filter(p => p.cat_psicosocial === 'Leve').length,
      Moderada: patientsWithPredictions.filter(p => p.cat_psicosocial === 'Moderada').length,
      Grave: patientsWithPredictions.filter(p => p.cat_psicosocial === 'Grave').length,
      Completa: patientsWithPredictions.filter(p => p.cat_psicosocial === 'Completa').length,
    },
  ];

  const COLORS = ['hsl(var(--chart-1))', 'hsl(var(--chart-2))', 'hsl(var(--chart-3))', 'hsl(var(--chart-4))', 'hsl(var(--chart-5))'];

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
        <h1 className="text-3xl font-bold">{t('analytics')}</h1>
        <p className="text-muted-foreground mt-2">
          Análisis detallado de predicciones y tendencias
        </p>
      </div>

      {patientsWithPredictions.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>Sin datos disponibles</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              No hay predicciones realizadas aún. Realiza predicciones para ver el análisis.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {/* Gráfica 1: Distribución de Perfiles de Predicción */}
          <Card>
            <CardHeader>
              <CardTitle>Distribución de Perfiles de Predicción</CardTitle>
              <p className="text-sm text-muted-foreground">
                Cantidad de pacientes por perfil de barrera
              </p>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={profileDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ perfil, cantidad, percent }) => 
                      `${perfil}: ${cantidad} (${(percent * 100).toFixed(0)}%)`
                    }
                    outerRadius={80}
                    fill="hsl(var(--primary))"
                    dataKey="cantidad"
                  >
                    {profileDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Estadísticas adicionales */}
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Resumen Estadístico</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-4">
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Total Pacientes</p>
                  <p className="text-2xl font-bold">{patients.length}</p>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Con Predicciones</p>
                  <p className="text-2xl font-bold">{patientsWithPredictions.length}</p>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Perfil Promedio</p>
                  <p className="text-2xl font-bold">
                    {patientsWithPredictions.length > 0
                      ? (patientsWithPredictions.reduce((sum, p) => sum + (p.prediction_profile || 0), 0) / patientsWithPredictions.length).toFixed(1)
                      : '0'}
                  </p>
                </div>
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Nivel Global Promedio</p>
                  <p className="text-2xl font-bold">
                    {patientsWithPredictions.length > 0
                      ? (patientsWithPredictions.reduce((sum, p) => sum + p.nivel_global, 0) / patientsWithPredictions.length).toFixed(1)
                      : '0'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
