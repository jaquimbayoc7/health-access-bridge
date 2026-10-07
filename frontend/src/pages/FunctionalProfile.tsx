import { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, Check, ClipboardCopy, Download, Loader2, Pencil, Sparkles, X } from 'lucide-react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { toast } from 'sonner';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { useLanguage } from '@/contexts/LanguageContext';
import { patientService, Patient } from '@/services/patients';
import { icfService, IcfItem, IcfSuggestionSet } from '@/services/icf';
import {
  DRAFT_NOTICE,
  LOCATION_LABELS,
  NATURE_LABELS,
  ORIGIN_LABELS,
  QUALIFIER_LABELS,
  RESOLUTION_HEADER,
  buildReportText,
  formatCode,
  qualifierText,
  reportSections,
} from '@/lib/icfReport';

const MIN_AGE = 6;
const DOMAIN_LABELS: Array<[keyof Patient, string]> = [
  ['nivel_d1', 'D1 Aprendizaje'],
  ['nivel_d2', 'D2 Tareas generales'],
  ['nivel_d3', 'D3 Comunicación'],
  ['nivel_d4', 'D4 Movilidad'],
  ['nivel_d5', 'D5 Autocuidado'],
  ['nivel_d6', 'D6 Vida doméstica'],
];

const STATUS_STYLE: Record<string, string> = {
  sugerido: 'bg-slate-200 text-slate-800',
  aceptado: 'bg-green-600 text-white',
  editado: 'bg-blue-600 text-white',
  rechazado: 'bg-red-600 text-white',
};

const STATUS_TEXT: Record<string, string> = {
  sugerido: 'Sugerido',
  aceptado: 'Aceptado',
  editado: 'Editado',
  rechazado: 'Rechazado',
};

export default function FunctionalProfile() {
  const { t, language } = useLanguage();
  const L = (es: string, en: string) => (language === 'es' ? es : en);

  const [patients, setPatients] = useState<Patient[]>([]);
  const [loadingPatients, setLoadingPatients] = useState(false);
  const [selectedId, setSelectedId] = useState('');
  const [diag, setDiag] = useState('');
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState<IcfSuggestionSet | null>(null);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<IcfItem | null>(null);
  const [editQ, setEditQ] = useState('');
  const [editCn, setEditCn] = useState('');
  const [editCl, setEditCl] = useState('');
  const [savingId, setSavingId] = useState<number | null>(null);

  const patient = useMemo(() => patients.find((p) => p.id === Number(selectedId)) ?? null, [patients, selectedId]);
  const tooYoung = patient !== null && patient.edad < MIN_AGE;

  useEffect(() => {
    (async () => {
      setLoadingPatients(true);
      try {
        setPatients(await patientService.getPatients());
      } catch {
        toast.error(L('Error al cargar pacientes', 'Error loading patients'));
      } finally {
        setLoadingPatients(false);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const hasItems = (set: IcfSuggestionSet | null) =>
    !!set && set.functions.length + set.structures.length + set.activities.length > 0;

  const handleSelect = async (id: string) => {
    setSelectedId(id);
    setResult(null);
    setError(null);
    try {
      const latest = await icfService.getLatest(Number(id));
      if (hasItems(latest)) setResult(latest);
    } catch {
      // sin sugerencia previa o sin acceso: se deja la pantalla en blanco
    }
  };

  const handleGenerate = async () => {
    if (!patient || tooYoung) return;
    setGenerating(true);
    setError(null);
    try {
      const set = await icfService.generate(patient.id, {
        ...(diag.trim() ? { diag_cie: diag.trim() } : {}),
        ...(notes.trim() ? { clinical_notes: notes.trim() } : {}),
      });
      setResult(set);
      set.warnings.forEach((w) => toast.warning(w));
      toast.success(L('Perfil funcional generado', 'Functional profile generated'));
    } catch (e) {
      setError(e instanceof Error ? e.message : L('No se pudo generar la sugerencia', 'Could not generate the suggestion'));
    } finally {
      setGenerating(false);
    }
  };

  const replaceItem = (updated: IcfItem) => {
    setResult((prev) => {
      if (!prev) return prev;
      const swap = (items: IcfItem[]) => items.map((i) => (i.id === updated.id ? updated : i));
      return { ...prev, functions: swap(prev.functions), structures: swap(prev.structures), activities: swap(prev.activities) };
    });
  };

  const decide = async (item: IcfItem, status: 'aceptado' | 'rechazado') => {
    setSavingId(item.id);
    try {
      replaceItem(await icfService.decide(item.id, { status }));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : L('No se pudo guardar la decisión', 'Could not save the decision'));
    } finally {
      setSavingId(null);
    }
  };

  const openEdit = (item: IcfItem) => {
    setEditing(item);
    setEditQ(item.qualifier === null ? '' : String(item.qualifier));
    setEditCn(String(item.qualifier_cn ?? 8));
    setEditCl(String(item.qualifier_cl ?? 8));
  };

  const saveEdit = async () => {
    if (!editing) return;
    setSavingId(editing.id);
    try {
      const body: Parameters<typeof icfService.decide>[1] = { status: 'editado' };
      if (editQ !== '') body.qualifier = Number(editQ);
      if (editing.component === 's') {
        body.qualifier_cn = Number(editCn);
        body.qualifier_cl = Number(editCl);
      }
      replaceItem(await icfService.decide(editing.id, body));
      setEditing(null);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : L('No se pudo guardar la edición', 'Could not save the edit'));
    } finally {
      setSavingId(null);
    }
  };

  const patientLabel = patient ? `${patient.nombre_apellidos}, ${patient.edad} ${L('años', 'years')}` : '';

  const copyReport = async () => {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(buildReportText(result, patientLabel));
      toast.success(L('Reporte copiado', 'Report copied'));
    } catch {
      toast.error(L('No se pudo copiar', 'Could not copy'));
    }
  };

  const downloadPdf = () => {
    if (!result) return;
    const doc = new jsPDF();
    doc.setFontSize(13);
    doc.text(`${RESOLUTION_HEADER}`, 14, 16);
    doc.setFontSize(11);
    doc.text('Perfil de funcionamiento (borrador de apoyo)', 14, 23);
    doc.text(`Paciente: ${patientLabel}`, 14, 30);
    let y = 36;
    for (const section of reportSections(result)) {
      autoTable(doc, {
        startY: y,
        head: [[section.title, 'Código', 'Calificador']],
        body: section.rows.length
          ? section.rows.map((r) => [r.title, formatCode(r), qualifierText(r)])
          : [['(sin códigos)', '', '']],
        headStyles: { fillColor: [43, 108, 176] },
        styles: { fontSize: 9 },
      });
      y = (doc as unknown as { lastAutoTable: { finalY: number } }).lastAutoTable.finalY + 6;
    }
    doc.setFontSize(8);
    doc.text(doc.splitTextToSize(DRAFT_NOTICE, 180), 14, y + 4);
    doc.save(`perfil-funcional-${patient?.id ?? 'paciente'}.pdf`);
  };

  const renderTable = (title: string, items: IcfItem[], isStructure = false) => (
    <Card key={title}>
      <CardHeader>
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <p className="text-sm text-muted-foreground">{L('Sin códigos sugeridos', 'No suggested codes')}</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{L('Código', 'Code')}</TableHead>
                <TableHead>{L('Título (catálogo CIF-IA)', 'Title (ICF-CY catalog)')}</TableHead>
                <TableHead>{L('Calificador', 'Qualifier')}</TableHead>
                <TableHead>{L('Justificación', 'Justification')}</TableHead>
                <TableHead>{L('Estado', 'Status')}</TableHead>
                <TableHead className="text-right">{L('Acciones', 'Actions')}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id} className={item.status === 'rechazado' ? 'opacity-50' : ''}>
                  <TableCell className="font-mono whitespace-nowrap" data-testid={`code-${item.id}`}>
                    {formatCode(item)}
                  </TableCell>
                  <TableCell>
                    {item.title}
                    <div className="mt-1">
                      <Badge variant="outline" className="text-xs">
                        {ORIGIN_LABELS[item.origin] ?? item.origin}
                      </Badge>
                    </div>
                  </TableCell>
                  <TableCell className="text-sm">{qualifierText(item)}</TableCell>
                  <TableCell className="text-sm text-muted-foreground max-w-[220px]">{item.justification || '—'}</TableCell>
                  <TableCell>
                    <Badge className={STATUS_STYLE[item.status]}>{STATUS_TEXT[item.status] ?? item.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right whitespace-nowrap">
                    <Button
                      size="icon"
                      variant="ghost"
                      aria-label={`${L('Aceptar', 'Accept')} ${item.code}`}
                      disabled={savingId === item.id}
                      onClick={() => decide(item, 'aceptado')}
                    >
                      <Check className="h-4 w-4 text-green-600" />
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      aria-label={`${L('Editar', 'Edit')} ${item.code}`}
                      disabled={savingId === item.id}
                      onClick={() => openEdit(item)}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      aria-label={`${L('Rechazar', 'Reject')} ${item.code}`}
                      disabled={savingId === item.id}
                      onClick={() => decide(item, 'rechazado')}
                    >
                      <X className="h-4 w-4 text-red-600" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
        {isStructure && items.length > 0 && (
          <p className="text-xs text-muted-foreground mt-3">
            {L(
              'Estructuras: magnitud, naturaleza del cambio y localización. Naturaleza y localización quedan «sin especificar» (8) por defecto: edítelas.',
              'Structures: extent, nature of change and location. Nature and location default to “unspecified” (8): edit them.'
            )}
          </p>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{t('functionalProfile')}</h1>
        <p className="text-muted-foreground mt-2">
          {L(
            `Sugerencia de códigos CIF-IA para el perfil de funcionamiento (${RESOLUTION_HEADER}).`,
            `Suggested ICF-CY codes for the functioning profile (${RESOLUTION_HEADER}).`
          )}
        </p>
      </div>

      <Alert>
        <AlertTriangle className="h-4 w-4" />
        <AlertTitle>{L('Borrador de apoyo', 'Support draft')}</AlertTitle>
        <AlertDescription>{DRAFT_NOTICE}</AlertDescription>
      </Alert>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>{L('Paciente y datos clínicos', 'Patient and clinical data')}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="fp-patient">{t('selectPatient')}</Label>
              <Select value={selectedId} onValueChange={handleSelect} disabled={loadingPatients}>
                <SelectTrigger id="fp-patient">
                  <SelectValue placeholder={t('selectPatient')} />
                </SelectTrigger>
                <SelectContent>
                  {patients.map((p) => (
                    <SelectItem key={p.id} value={String(p.id)}>
                      {p.nombre_apellidos} — {p.edad} {L('años', 'years')}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {patient && (
              <div className="p-4 bg-muted rounded-lg text-sm space-y-1" data-testid="patient-summary">
                <p><strong>{L('Causa', 'Cause')}:</strong> {patient.causa_deficiencia}</p>
                <p>
                  <strong>{L('Física', 'Physical')}:</strong> {patient.cat_fisica} · <strong>{L('Psicosocial', 'Psychosocial')}:</strong>{' '}
                  {patient.cat_psicosocial}
                </p>
                <div className="grid grid-cols-2 gap-x-4">
                  {DOMAIN_LABELS.map(([key, label]) => (
                    <span key={key}>{label}: {String(patient[key])}</span>
                  ))}
                </div>
                <p>
                  <strong>{L('Predicción de barreras', 'Barrier prediction')}:</strong>{' '}
                  {patient.prediction_description ?? L('sin predicción (se genera igual)', 'no prediction (generated anyway)')}
                </p>
                <p className="text-xs text-muted-foreground">
                  {L(
                    'Al servicio solo viajan edad, género, causa, categorías, niveles D1–D6, la predicción y los campos de abajo. Nunca el nombre, el documento ni la orientación sexual.',
                    'Only age, gender, cause, categories, D1–D6 levels, the prediction and the fields below are sent. Never name, ID or sexual orientation.'
                  )}
                </p>
              </div>
            )}

            {tooYoung && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  {L(
                    'Para pacientes menores de 6 años no aplica la sugerencia basada en los niveles D1–D6.',
                    'The D1–D6 based suggestion does not apply to patients under 6 years old.'
                  )}
                </AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="fp-diag">{L('Diagnóstico CIE (opcional)', 'ICD diagnosis (optional)')}</Label>
              <Input
                id="fp-diag"
                value={diag}
                maxLength={300}
                placeholder="G80 Parálisis cerebral"
                onChange={(e) => setDiag(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="fp-notes">{L('Notas clínicas (opcional)', 'Clinical notes (optional)')}</Label>
              <Textarea
                id="fp-notes"
                value={notes}
                maxLength={2000}
                rows={4}
                onChange={(e) => setNotes(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                {L(
                  'No incluya datos que identifiquen a la persona (nombre, documento, dirección, teléfono). Sin diagnóstico ni notas, las funciones y estructuras serán genéricas.',
                  'Do not include identifying data (name, ID, address, phone). Without a diagnosis or notes, functions and structures will be generic.'
                )}
              </p>
            </div>

            <Button className="w-full gap-2" onClick={handleGenerate} disabled={!patient || tooYoung || generating}>
              {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              {generating ? L('Generando…', 'Generating…') : L('Generar Perfil Funcional', 'Generate Functional Profile')}
            </Button>
            {generating && (
              <p className="text-xs text-muted-foreground" role="status">
                {L('Puede tardar unos segundos (hasta 90 s si el equipo está ocupado).', 'It may take a few seconds (up to 90 s if the machine is busy).')}
              </p>
            )}
          </CardContent>
        </Card>

        <div className="space-y-4">
          {error && (
            <Alert variant="destructive" role="alert">
              <AlertTriangle className="h-4 w-4" />
              <AlertTitle>{L('No se pudo generar el perfil', 'Could not generate the profile')}</AlertTitle>
              <AlertDescription>
                {error} {L('El resto de la aplicación sigue funcionando.', 'The rest of the application keeps working.')}
              </AlertDescription>
            </Alert>
          )}
          {result && hasItems(result) ? (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">{L('Resumen', 'Summary')}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm space-y-2">
                <p>
                  {L('Generado con', 'Generated with')}: <strong>{result.model ?? '—'}</strong>
                  {!result.llm_used && ` (${L('por similitud, sin el modelo', 'by similarity, without the model')})`}
                  {result.latency_ms !== null && ` · ${(result.latency_ms / 1000).toFixed(1)} s`}
                </p>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="gap-2" onClick={copyReport}>
                    <ClipboardCopy className="h-4 w-4" />
                    {L('Copiar', 'Copy')}
                  </Button>
                  <Button variant="outline" size="sm" className="gap-2" onClick={downloadPdf}>
                    <Download className="h-4 w-4" />
                    {L('Descargar PDF', 'Download PDF')}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            !error && (
              <Card>
                <CardContent className="py-10 text-center text-sm text-muted-foreground">
                  {patient
                    ? L('Aún no hay un perfil funcional para este paciente.', 'There is no functional profile for this patient yet.')
                    : L('Seleccione un paciente para empezar.', 'Select a patient to start.')}
                </CardContent>
              </Card>
            )
          )}
        </div>
      </div>

      {result && hasItems(result) && (
        <div className="space-y-4">
          {renderTable(L('Funciones corporales (b)', 'Body functions (b)'), result.functions)}
          {renderTable(L('Estructuras corporales (s)', 'Body structures (s)'), result.structures, true)}
          {renderTable(L('Actividades y participación (d)', 'Activities and participation (d)'), result.activities)}
        </div>
      )}

      <Dialog open={editing !== null} onOpenChange={(open) => !open && setEditing(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {L('Editar calificador', 'Edit qualifier')} {editing?.code}
            </DialogTitle>
            <DialogDescription>{editing?.title}</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="edit-q">
                {editing?.component === 's' ? L('Magnitud', 'Extent') : L('Calificador', 'Qualifier')}
              </Label>
              <Select value={editQ} onValueChange={setEditQ}>
                <SelectTrigger id="edit-q">
                  <SelectValue placeholder="—" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(QUALIFIER_LABELS).map(([value, label]) => (
                    <SelectItem key={value} value={value}>{value} — {label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            {editing?.component === 's' && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="edit-cn">{L('Naturaleza del cambio', 'Nature of change')}</Label>
                  <Select value={editCn} onValueChange={setEditCn}>
                    <SelectTrigger id="edit-cn"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      {Object.entries(NATURE_LABELS).map(([value, label]) => (
                        <SelectItem key={value} value={value}>{value} — {label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-cl">{L('Localización', 'Location')}</Label>
                  <Select value={editCl} onValueChange={setEditCl}>
                    <SelectTrigger id="edit-cl"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      {Object.entries(LOCATION_LABELS).map(([value, label]) => (
                        <SelectItem key={value} value={value}>{value} — {label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditing(null)}>{L('Cancelar', 'Cancel')}</Button>
            <Button onClick={saveEdit} disabled={savingId !== null}>{L('Guardar', 'Save')}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
