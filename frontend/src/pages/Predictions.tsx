import { useState, useEffect } from 'react';
import { Play, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { useLanguage } from '@/contexts/LanguageContext';
import { patientService, Patient } from '@/services/patients';
import { toast } from 'sonner';

export default function Predictions() {
  const { t, language } = useLanguage();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPredicting, setIsPredicting] = useState(false);
  const [patientsWithPredictions, setPatientsWithPredictions] = useState<Patient[]>([]);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    setIsLoading(true);
    try {
      const data = await patientService.getPatients();
      setPatients(data);
      setPatientsWithPredictions(data.filter(p => p.prediction_profile !== null));
    } catch (error) {
      toast.error(language === 'es' ? 'Error al cargar pacientes' : 'Error loading patients');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRunPrediction = async () => {
    if (!selectedPatientId) {
      toast.error(language === 'es' ? 'Por favor seleccione un paciente' : 'Please select a patient');
      return;
    }

    setIsPredicting(true);
    try {
      const result = await patientService.predictPatient(Number(selectedPatientId));
      toast.success(
        language === 'es' 
          ? `Predicción completada: Perfil ${result.profile}` 
          : `Prediction completed: Profile ${result.profile}`
      );
      loadPatients();
      setSelectedPatientId('');
    } catch (error) {
      toast.error(language === 'es' ? 'Error en la predicción' : 'Prediction error');
    } finally {
      setIsPredicting(false);
    }
  };

  const getProfileColor = (profile: number) => {
    const colors = [
      'bg-green-500',
      'bg-blue-500',
      'bg-yellow-500',
      'bg-orange-500',
      'bg-red-500'
    ];
    return colors[profile - 1] || 'bg-gray-500';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">{t('predictions')}</h1>
          <p className="text-muted-foreground mt-2">
            Run disability barrier predictions for patients
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>{t('newPrediction')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="patient">{t('selectPatient')}</Label>
                <Select value={selectedPatientId} onValueChange={setSelectedPatientId}>
                  <SelectTrigger id="patient">
                    <SelectValue placeholder={t('selectPatient')} />
                  </SelectTrigger>
                  <SelectContent>
                    {patients.map((patient) => (
                      <SelectItem key={patient.id} value={patient.id.toString()}>
                        {patient.nombre_apellidos} - {language === 'es' ? 'Edad' : 'Age'}: {patient.edad}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {selectedPatientId && (
                <div className="p-4 bg-muted rounded-lg space-y-2">
                  <h4 className="font-medium">
                    {language === 'es' ? 'Información del Paciente' : 'Patient Information'}
                  </h4>
                  {(() => {
                    const selected = patients.find(p => p.id === Number(selectedPatientId));
                    return selected ? (
                      <div className="text-sm text-muted-foreground space-y-1">
                        <p><strong>{language === 'es' ? 'Nombre' : 'Name'}:</strong> {selected.nombre_apellidos}</p>
                        <p><strong>{language === 'es' ? 'Edad' : 'Age'}:</strong> {selected.edad}</p>
                        <p><strong>{language === 'es' ? 'Género' : 'Gender'}:</strong> {selected.genero}</p>
                        <p><strong>{language === 'es' ? 'Nivel Global' : 'Global Level'}:</strong> {selected.nivel_global}</p>
                      </div>
                    ) : null;
                  })()}
                </div>
              )}

              <Button 
                className="w-full gap-2" 
                onClick={handleRunPrediction}
                disabled={!selectedPatientId || isPredicting}
              >
                <Play className="h-4 w-4" />
                {isPredicting 
                  ? (language === 'es' ? 'Ejecutando...' : 'Running...') 
                  : t('runPrediction')}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('predictionHistory')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {isLoading ? (
                <p className="text-sm text-muted-foreground text-center py-8">{t('loading')}</p>
              ) : patientsWithPredictions.length === 0 ? (
                <div className="text-center py-8">
                  <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-2" />
                  <p className="text-sm text-muted-foreground">
                    {language === 'es' ? 'No hay predicciones aún' : 'No predictions yet'}
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {patientsWithPredictions.map((patient) => (
                    <div key={patient.id} className="p-4 border rounded-lg space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{patient.nombre_apellidos}</span>
                        <Badge className={getProfileColor(patient.prediction_profile!)}>
                          {language === 'es' ? 'Perfil' : 'Profile'} {patient.prediction_profile}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {patient.prediction_description}
                      </p>
                      <div className="text-xs text-muted-foreground">
                        {language === 'es' ? 'Nivel Global' : 'Global Level'}: {patient.nivel_global}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}