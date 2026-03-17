import { useState, useEffect } from 'react';
import { Plus, Search, Edit, Trash2, Download, FileSpreadsheet } from 'lucide-react';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useLanguage } from '@/contexts/LanguageContext';
import { useAuth } from '@/contexts/AuthContext';
import { patientService, Patient, PatientCreate } from '@/services/patients';
import { toast } from 'sonner';

export default function Patients() {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
  const [deletePatient, setDeletePatient] = useState<Patient | null>(null);

  // Form state
  const [formData, setFormData] = useState<PatientCreate>({
    nombre_apellidos: '',
    numero_documento: '',
    fecha_nacimiento: '',
    edad: 0,
    genero: '',
    orientacion_sexual: '',
    causa_deficiencia: '',
    cat_fisica: '',
    cat_psicosocial: '',
    nivel_d1: 0,
    nivel_d2: 0,
    nivel_d3: 0,
    nivel_d4: 0,
    nivel_d5: 0,
    nivel_d6: 0,
    nivel_global: 0,
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      loadPatients(searchQuery);
    }, 400);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const loadPatients = async (search: string = '') => {
    setIsLoading(true);
    try {
      const data = await patientService.getPatients(0, 100, search);
      setPatients(data);
    } catch (error) {
      toast.error(t('errorLoadingPatients'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenDialog = (patient?: Patient) => {
    if (patient) {
      setEditingPatient(patient);
      setFormData({
        nombre_apellidos: patient.nombre_apellidos,
        numero_documento: patient.numero_documento,
        fecha_nacimiento: patient.fecha_nacimiento,
        edad: patient.edad,
        genero: patient.genero,
        orientacion_sexual: patient.orientacion_sexual,
        causa_deficiencia: patient.causa_deficiencia,
        cat_fisica: patient.cat_fisica,
        cat_psicosocial: patient.cat_psicosocial,
        nivel_d1: patient.nivel_d1,
        nivel_d2: patient.nivel_d2,
        nivel_d3: patient.nivel_d3,
        nivel_d4: patient.nivel_d4,
        nivel_d5: patient.nivel_d5,
        nivel_d6: patient.nivel_d6,
        nivel_global: patient.nivel_global,
      });
    } else {
      setEditingPatient(null);
      setFormData({
        nombre_apellidos: '',
        numero_documento: '',
        fecha_nacimiento: '',
        edad: 0,
        genero: '',
        orientacion_sexual: '',
        causa_deficiencia: '',
        cat_fisica: '',
        cat_psicosocial: '',
        nivel_d1: 0,
        nivel_d2: 0,
        nivel_d3: 0,
        nivel_d4: 0,
        nivel_d5: 0,
        nivel_d6: 0,
        nivel_global: 0,
      });
    }
    setIsDialogOpen(true);
  };

  const handleSavePatient = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validar que todos los niveles estén entre 0 y 100
    const levels = [
      formData.nivel_d1,
      formData.nivel_d2,
      formData.nivel_d3,
      formData.nivel_d4,
      formData.nivel_d5,
      formData.nivel_d6
    ];

    const invalidLevels = levels.some(level => level < 0 || level > 100);

    if (invalidLevels) {
      toast.error('Todos los niveles deben estar entre 0 y 100');
      return;
    }

    try {
      if (editingPatient) {
        await patientService.updatePatient(editingPatient.id, formData);
        toast.success(t('patientUpdated'));
      } else {
        await patientService.createPatient(formData);
        toast.success(t('patientCreated'));
      }
      setIsDialogOpen(false);
      loadPatients();
    } catch (error) {
      toast.error(editingPatient ? t('errorUpdatingPatient') : t('errorCreatingPatient'));
    }
  };

  const handleDeletePatient = async () => {
    if (!deletePatient) return;
    try {
      await patientService.deletePatient(deletePatient.id);
      toast.success(t('patientDeleted'));
      setDeletePatient(null);
      loadPatients();
    } catch (error) {
      toast.error(t('errorDeletingPatient'));
    }
  };

  const filteredPatients = patients;

  const handleExportExcel = () => {
    const now = new Date();
    const fechaHora = now.toLocaleString('es-ES', { 
      dateStyle: 'full', 
      timeStyle: 'short' 
    });

    const dataToExport = filteredPatients.map(patient => ({
      'Nombre y Apellidos': patient.nombre_apellidos,
      'Nº Documento': patient.numero_documento,
      'Edad': patient.edad,
      'Género': patient.genero,
      'Causa de Deficiencia': patient.causa_deficiencia,
      'Categoría Física': patient.cat_fisica,
      'Categoría Psicosocial': patient.cat_psicosocial,
      'Nivel Global': patient.nivel_global,
    }));

    const ws = XLSX.utils.json_to_sheet(dataToExport);

    // Agregar información del reporte al final
    const range = XLSX.utils.decode_range(ws['!ref'] || 'A1');
    const startRow = range.e.r + 2; // Dos filas después de los datos

    XLSX.utils.sheet_add_aoa(ws, [
      [], // Fila vacía para separación
      ['REPORTE DE PACIENTES'],
      ['Fecha y Hora del Reporte:', fechaHora],
      ['Médico Tratante:', `Dr. ${user?.name || user?.email || 'No disponible'}`],
    ], { origin: `A${startRow}` });

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Pacientes');
    XLSX.writeFile(wb, `pacientes_${now.toISOString().split('T')[0]}.xlsx`);
    toast.success('Archivo Excel descargado exitosamente');
  };

  const handleExportPDF = () => {
    const now = new Date();
    const fechaHora = now.toLocaleString('es-ES', { 
      dateStyle: 'full', 
      timeStyle: 'short' 
    });

    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();

    // Agregar información del reporte centrada antes de la tabla
    doc.setFontSize(14);
    const titulo = 'REPORTE DE PACIENTES';
    const tituloWidth = doc.getTextWidth(titulo);
    doc.text(titulo, (pageWidth - tituloWidth) / 2, 20);

    doc.setFontSize(10);
    const fecha = `Fecha y Hora del Reporte: ${fechaHora}`;
    const fechaWidth = doc.getTextWidth(fecha);
    doc.text(fecha, (pageWidth - fechaWidth) / 2, 28);

    const medico = `Médico Tratante: Dr. ${user?.name || user?.email || 'No disponible'}`;
    const medicoWidth = doc.getTextWidth(medico);
    doc.text(medico, (pageWidth - medicoWidth) / 2, 35);

    const tableData = filteredPatients.map(patient => [
      patient.nombre_apellidos,
      patient.numero_documento,
      patient.edad,
      patient.genero,
      patient.causa_deficiencia,
      patient.cat_fisica,
      patient.cat_psicosocial,
      patient.nivel_global,
    ]);

    autoTable(doc, {
      head: [['Nombre', 'Nº Documento', 'Edad', 'Género', 'Causa Deficiencia', 'Cat. Física', 'Cat. Psicosocial', 'Nivel Global']],
      body: tableData,
      startY: 45,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [59, 130, 246] },
    });

    doc.save(`pacientes_${now.toISOString().split('T')[0]}.pdf`);
    toast.success('Archivo PDF descargado exitosamente');
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">{t('patients')}</h1>
          <p className="text-muted-foreground mt-2">
            Manage patient records and information
          </p>
        </div>
        <Button className="gap-2" onClick={() => handleOpenDialog()}>
          <Plus className="h-4 w-4" />
          {t('addPatient')}
        </Button>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="flex gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder={t('search')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={handleExportExcel}
              disabled={filteredPatients.length === 0}
            >
              <FileSpreadsheet className="h-4 w-4" />
              Excel
            </Button>
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={handleExportPDF}
              disabled={filteredPatients.length === 0}
            >
              <Download className="h-4 w-4" />
              PDF
            </Button>
          </div>

          {isLoading ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">{t('loading')}</p>
            </div>
          ) : filteredPatients.length === 0 ? (
            <div className="text-center py-12">
              <div className="mb-4">
                <div className="mx-auto w-16 h-16 bg-muted rounded-full flex items-center justify-center">
                  <Plus className="h-8 w-8 text-muted-foreground" />
                </div>
              </div>
              <h3 className="text-lg font-medium mb-2">{t('noPatientsYet')}</h3>
              <p className="text-muted-foreground mb-4">{t('addFirstPatient')}</p>
              <Button onClick={() => handleOpenDialog()}>
                <Plus className="h-4 w-4 mr-2" />
                {t('addPatient')}
              </Button>
            </div>
          ) : (
            <>
              {/* Desktop Table - Hidden on mobile */}
              <div className="hidden md:block overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>{t('patientName')}</TableHead>
                      <TableHead>Nº Documento</TableHead>
                      <TableHead>{t('age')}</TableHead>
                      <TableHead>{t('gender')}</TableHead>
                      <TableHead>{t('deficiencyCause')}</TableHead>
                      <TableHead>Cat. Física</TableHead>
                      <TableHead>Cat. Psicosocial</TableHead>
                      <TableHead>{t('globalLevel')}</TableHead>
                      <TableHead className="text-right">{t('actions')}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredPatients.map((patient) => (
                      <TableRow key={patient.id}>
                        <TableCell className="font-medium">{patient.nombre_apellidos}</TableCell>
                        <TableCell>{patient.numero_documento}</TableCell>
                        <TableCell>{patient.edad}</TableCell>
                        <TableCell>{patient.genero}</TableCell>
                        <TableCell>{patient.causa_deficiencia}</TableCell>
                        <TableCell>{patient.cat_fisica}</TableCell>
                        <TableCell>{patient.cat_psicosocial}</TableCell>
                        <TableCell>{patient.nivel_global}</TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-2">
                            <Button 
                              variant="ghost" 
                              size="icon"
                              onClick={() => handleOpenDialog(patient)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="icon"
                              onClick={() => setDeletePatient(patient)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              {/* Mobile Cards - Shown only on mobile */}
              <div className="md:hidden space-y-4">
                {filteredPatients.map((patient) => (
                  <Card key={patient.id} className="overflow-hidden">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg">{patient.nombre_apellidos}</h3>
                          <p className="text-sm text-muted-foreground">
                            {patient.edad} {t('age')} · {patient.genero}
                          </p>
                        </div>
                        <div className="flex gap-1">
                          <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => handleOpenDialog(patient)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => setDeletePatient(patient)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">{t('deficiencyCause')}:</span>
                          <span className="font-medium text-right">{patient.causa_deficiencia}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Cat. Física:</span>
                          <span className="font-medium">{patient.cat_fisica}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Cat. Psicosocial:</span>
                          <span className="font-medium">{patient.cat_psicosocial}</span>
                        </div>
                        <div className="flex justify-between pt-2 border-t">
                          <span className="text-muted-foreground font-medium">{t('globalLevel')}:</span>
                          <span className="font-bold text-primary">{patient.nivel_global}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Create/Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingPatient ? t('editPatient') : t('createPatient')}</DialogTitle>
            <DialogDescription>
              Complete all the required information about the patient.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSavePatient} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="nombre_apellidos">{t('fullName')}</Label>
                <Input
                  id="nombre_apellidos"
                  value={formData.nombre_apellidos}
                  onChange={(e) => setFormData({ ...formData, nombre_apellidos: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="numero_documento">Nº Documento</Label>
                <Input
                  id="numero_documento"
                  placeholder="Ej: 1001234567"
                  value={formData.numero_documento}
                  onChange={(e) => setFormData({ ...formData, numero_documento: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="fecha_nacimiento">{t('birthDate')}</Label>
                <Input
                  id="fecha_nacimiento"
                  type="date"
                  value={formData.fecha_nacimiento}
                  onChange={(e) => {
                    const newDate = e.target.value;
                    const calculatedAge = newDate ? Math.floor((new Date().getTime() - new Date(newDate).getTime()) / (365.25 * 24 * 60 * 60 * 1000)) : 0;
                    setFormData({ ...formData, fecha_nacimiento: newDate, edad: calculatedAge });
                  }}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="edad">{t('age')}</Label>
                <Input
                  id="edad"
                  type="number"
                  value={formData.edad}
                  disabled
                  className="bg-muted cursor-not-allowed"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="genero">{t('gender')}</Label>
                <Select value={formData.genero} onValueChange={(value) => setFormData({ ...formData, genero: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder={t('gender')} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="masculino">{t('male')}</SelectItem>
                    <SelectItem value="femenino">{t('female')}</SelectItem>
                    <SelectItem value="otro">{t('other')}</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="orientacion_sexual">{t('sexualOrientation')}</Label>
                <Input
                  id="orientacion_sexual"
                  value={formData.orientacion_sexual}
                  onChange={(e) => setFormData({ ...formData, orientacion_sexual: e.target.value })}
                  required
                />
              </div>

              <div className="col-span-2 space-y-2">
                <Label htmlFor="causa_deficiencia">{t('deficiencyCause')}</Label>
                <Select value={formData.causa_deficiencia} onValueChange={(value) => setFormData({ ...formData, causa_deficiencia: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder={t('deficiencyCause')} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Enfermedad general">Enfermedad general</SelectItem>
                    <SelectItem value="Accidente de tránsito">Accidente de tránsito</SelectItem>
                    <SelectItem value="Alteración genética o hereditaria">Alteración genética o hereditaria</SelectItem>
                    <SelectItem value="Complicaciones durante el parto">Complicaciones durante el parto</SelectItem>
                    <SelectItem value="Violencia por delincuencia común">Violencia por delincuencia común</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="cat_fisica">{t('physicalCategory')}</Label>
                <Select value={formData.cat_fisica} onValueChange={(value) => setFormData({ ...formData, cat_fisica: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder={t('physicalCategory')} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Sí">Sí</SelectItem>
                    <SelectItem value="No">No</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="cat_psicosocial">{t('psychosocialCategory')}</Label>
                <Select value={formData.cat_psicosocial} onValueChange={(value) => setFormData({ ...formData, cat_psicosocial: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder={t('psychosocialCategory')} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Sí">Sí</SelectItem>
                    <SelectItem value="No">No</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d1">{t('levelD1')}</Label>
                <Input
                  id="nivel_d1"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d1}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d1: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d2">{t('levelD2')}</Label>
                <Input
                  id="nivel_d2"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d2}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d2: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d3">{t('levelD3')}</Label>
                <Input
                  id="nivel_d3"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d3}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d3: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d4">{t('levelD4')}</Label>
                <Input
                  id="nivel_d4"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d4}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d4: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d5">{t('levelD5')}</Label>
                <Input
                  id="nivel_d5"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d5}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d5: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_d6">{t('levelD6')}</Label>
                <Input
                  id="nivel_d6"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.nivel_d6}
                  onChange={(e) => {
                    const newValue = Number(e.target.value);
                    const newFormData = { ...formData, nivel_d6: newValue };
                    const avg = (newFormData.nivel_d1 + newFormData.nivel_d2 + newFormData.nivel_d3 + newFormData.nivel_d4 + newFormData.nivel_d5 + newFormData.nivel_d6) / 6;
                    setFormData({ ...newFormData, nivel_global: Math.round(avg) });
                  }}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="nivel_global">{t('globalLevel')}</Label>
                <Input
                  id="nivel_global"
                  type="number"
                  value={formData.nivel_global}
                  disabled
                  className="bg-muted cursor-not-allowed"
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                {t('cancel')}
              </Button>
              <Button type="submit">{t('save')}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={!!deletePatient} onOpenChange={() => setDeletePatient(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t('confirmDelete')}</AlertDialogTitle>
            <AlertDialogDescription>
              {t('deleteWarning')}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t('cancel')}</AlertDialogCancel>
            <AlertDialogAction onClick={handleDeletePatient}>
              {t('delete')}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}