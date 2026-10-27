import { useCallback, useEffect, useMemo, useRef, useState, type ReactElement, type ReactNode } from 'react';
import { FileSpreadsheet, FileText, Loader2, RefreshCw, ShieldCheck } from 'lucide-react';
import { toast } from 'sonner';
import {
  Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar,
  RadarChart, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAuth } from '@/contexts/AuthContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { apiService } from '@/services/api';
import {
  analyticsService, type AnalyticsFilterOptions, type AnalyticsFilters, type AnalyticsSummary, type CountEntry,
} from '@/services/analytics';
import { analyticsLabels, formatNumber, formatPercent, type Labels } from '@/lib/analyticsLabels';
import { exportExcel, exportPdf, svgToImage, type ChartImage } from '@/lib/analyticsExport';

// Paleta de Okabe e Ito (distinguible con daltonismo) en hexadecimal: los SVG que se exportan al PDF no resuelven variables CSS.
const PALETTE = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7', '#56B4E9', '#F0E442', '#666666'];
const STATUS_COLOR = { aceptado: '#009E73', editado: '#56B4E9', rechazado: '#D55E00', sugerido: '#999999' } as const;
const EMPTY_FILTERS: AnalyticsFilters = { genero: '', causa: '', perfil: '', edad_min: '', edad_max: '', owner_id: '' };

interface ChartDef {
  id: string;
  title: string;
  note?: string;
  render: (size?: { width: number; height: number }) => ReactElement;
}

function Chart({ size, height = 260, children }: { size?: { width: number; height: number }; height?: number; children: ReactElement }) {
  if (size) return <div style={{ width: size.width, height: size.height }}>{children}</div>;
  return <ResponsiveContainer width="100%" height={height}>{children}</ResponsiveContainer>;
}

function buildCharts(summary: AnalyticsSummary, L: Labels): { patients: ChartDef[]; icf: ChartDef[] } {
  const d = summary.distributions;
  const pie = (id: string, title: string, data: CountEntry[]): ChartDef => ({
    id, title,
    render: (size) => (
      <Chart size={size}>
        <PieChart width={size?.width} height={size?.height}>
          <Pie data={data} dataKey="count" nameKey="key" outerRadius="70%" isAnimationActive={false}
               label={({ name, value }) => `${name}: ${value}`}>
            {data.map((d, i) => <Cell key={i} fill={PALETTE[i % PALETTE.length]} aria-label={`${d.key}: ${d.count}`} />)}
          </Pie>
          <Tooltip />
        </PieChart>
      </Chart>
    ),
  });
  const bars = (id: string, title: string, data: CountEntry[], horizontal = false): ChartDef => ({
    id, title,
    render: (size) => (
      <Chart size={size} height={horizontal ? Math.max(220, data.length * 34) : 260}>
        <BarChart data={data} layout={horizontal ? 'vertical' : 'horizontal'} width={size?.width} height={size?.height}
                  margin={{ left: horizontal ? 40 : 0, right: 16 }}>
          <CartesianGrid strokeDasharray="3 3" />
          {horizontal ? (
            <>
              <XAxis type="number" allowDecimals={false} />
              <YAxis type="category" dataKey="key" width={150} tick={{ fontSize: 11 }} />
            </>
          ) : (
            <>
              <XAxis dataKey="key" tick={{ fontSize: 11 }} />
              <YAxis allowDecimals={false} />
            </>
          )}
          <Tooltip />
          <Bar dataKey="count" name={L.patientsAxis} fill={PALETTE[0]} isAnimationActive={false} />
        </BarChart>
      </Chart>
    ),
  });

  const domains: ChartDef = {
    id: 'domains', title: L.chDomains,
    render: (size) => (
      <Chart size={size}>
        <RadarChart data={summary.domains.map((x) => ({ domain: x.domain, mean: x.mean ?? 0 }))}
                    width={size?.width} height={size?.height}>
          <PolarGrid />
          <PolarAngleAxis dataKey="domain" />
          <PolarRadiusAxis domain={[0, 100]} />
          <Radar name={L.colMean} dataKey="mean" stroke={PALETTE[0]} fill={PALETTE[0]} fillOpacity={0.35} isAnimationActive={false} />
          <Tooltip />
        </RadarChart>
      </Chart>
    ),
  };

  const statusData = (['b', 's', 'd'] as const).map((c) => ({ name: L[c], ...summary.icf.by_component[c] }));
  const status: ChartDef = {
    id: 'status', title: L.chStatus, note: L.statusLegend,
    render: (size) => (
      <Chart size={size}>
        <BarChart data={statusData} width={size?.width} height={size?.height}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fontSize: 11 }} />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          {(['aceptado', 'editado', 'rechazado', 'sugerido'] as const).map((s) => (
            <Bar key={s} dataKey={s} name={L[s]} stackId="status" fill={STATUS_COLOR[s]} isAnimationActive={false} />
          ))}
        </BarChart>
      </Chart>
    ),
  };

  return {
    patients: [
      pie('profile', L.chProfile, d.profile),
      bars('fisica', L.chFisica, d.cat_fisica),
      bars('psico', L.chPsicosocial, d.cat_psicosocial),
      pie('genero', L.chGenero, d.genero),
      bars('age', L.chAge, d.age_group),
      bars('cause', L.chCause, d.cause, true),
      domains,
    ],
    icf: [status, pie('origin', L.chOrigin, summary.icf.by_origin), bars('model', L.chModel, summary.icf.by_model)],
  };
}

function Kpi({ label, value, help, testId }: { label: string; value: string | number; help?: string; testId: string }) {
  return (
    <Card>
      <CardContent className="p-4">
        <p className="text-sm font-medium text-muted-foreground">{label}</p>
        <p className="text-2xl font-bold" data-testid={testId}>{value}</p>
        {help && <p className="text-xs text-muted-foreground mt-1">{help}</p>}
      </CardContent>
    </Card>
  );
}

function FilterSelect({ id, label, value, onChange, children }: {
  id: string; label: string; value: string; onChange: (v: string) => void; children: ReactNode;
}) {
  return (
    <div className="space-y-1">
      <label htmlFor={id} className="text-xs font-medium text-muted-foreground">{label}</label>
      <select id={id} value={value} onChange={(e) => onChange(e.target.value)}
              className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm">
        {children}
      </select>
    </div>
  );
}

export default function Analytics() {
  const { language } = useLanguage();
  const { user } = useAuth();
  const L = useMemo(() => analyticsLabels(language === 'en' ? 'en' : 'es'), [language]);
  const lang = language === 'en' ? 'en' : 'es';
  const isAdmin = user?.role === 'admin';

  const [filters, setFilters] = useState<AnalyticsFilters>(EMPTY_FILTERS);
  const [applied, setApplied] = useState<AnalyticsFilters>(EMPTY_FILTERS);
  const [options, setOptions] = useState<AnalyticsFilterOptions | null>(null);
  const [doctors, setDoctors] = useState<{ id: number; full_name: string }[]>([]);
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exporting, setExporting] = useState<'xlsx' | 'pdf' | null>(null);
  const [offscreen, setOffscreen] = useState(false);
  const offscreenRef = useRef<HTMLDivElement>(null);

  const load = useCallback(async (f: AnalyticsFilters) => {
    setLoading(true);
    setError(null);
    try {
      setSummary(await analyticsService.getSummary(f));
    } catch (e) {
      setError(e instanceof Error ? e.message : L.loadError);
    } finally {
      setLoading(false);
    }
  }, [L.loadError]);

  useEffect(() => { void load(applied); }, [applied, load]);

  useEffect(() => {
    analyticsService.getFilterOptions().then(setOptions).catch(() => setOptions(null));
    if (isAdmin) {
      apiService.getUsers().then((users) =>
        setDoctors(users.filter((u) => u.role === 'médico').map((u) => ({ id: u.id, full_name: u.full_name })))
      ).catch(() => setDoctors([]));
    }
  }, [isAdmin]);

  // Los selectores aplican de inmediato; las edades esperan un momento para no consultar en cada tecla.
  const setFilter = (key: keyof AnalyticsFilters, value: string, immediate = true) => {
    const next = { ...filters, [key]: value };
    setFilters(next);
    if (immediate) setApplied(next);
  };
  useEffect(() => {
    const id = setTimeout(() => {
      if (filters.edad_min !== applied.edad_min || filters.edad_max !== applied.edad_max) setApplied(filters);
    }, 500);
    return () => clearTimeout(id);
  }, [filters, applied]);

  const clear = () => { setFilters(EMPTY_FILTERS); setApplied(EMPTY_FILTERS); };
  const hasFilters = Object.values(applied).some((v) => v);
  const charts = useMemo(() => (summary ? buildCharts(summary, L) : null), [summary, L]);

  const handleExcel = () => {
    if (!summary) return;
    try {
      setExporting('xlsx');
      exportExcel(summary, lang);
      toast.success(L.excelOk);
    } catch {
      toast.error(L.exportError);
    } finally {
      setExporting(null);
    }
  };

  const handlePdf = async () => {
    if (!summary || !charts) return;
    setExporting('pdf');
    setOffscreen(true); // monta los gráficos con tamaño fijo fuera de pantalla para rasterizarlos
    try {
      await new Promise((resolve) => setTimeout(resolve, 150));
      const images: ChartImage[] = [];
      const nodes = offscreenRef.current?.querySelectorAll<HTMLElement>('[data-chart-title]') ?? [];
      for (const node of Array.from(nodes)) {
        const svg = node.querySelector<SVGSVGElement>('svg.recharts-surface');
        if (svg) images.push({ title: node.dataset.chartTitle ?? '', note: node.dataset.chartNote, ...(await svgToImage(svg)) });
      }
      exportPdf(summary, lang, images);
      toast.success(L.pdfOk);
    } catch {
      toast.error(L.exportError);
    } finally {
      setOffscreen(false);
      setExporting(null);
    }
  };

  const renderGrid = (defs: ChartDef[]) => (
    <div className="grid gap-6 md:grid-cols-2">
      {defs.map((c) => (
        <Card key={c.id} className={c.id === 'cause' ? 'md:col-span-2' : undefined}>
          <CardHeader><CardTitle className="text-base">{c.title}</CardTitle></CardHeader>
          <CardContent role="img" aria-label={c.title}>{c.render()}</CardContent>
        </Card>
      ))}
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">{L.title}</h1>
          <p className="text-muted-foreground mt-2">{L.subtitle}</p>
          <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
            <ShieldCheck className="h-3.5 w-3.5" /> {L.privacy}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2" onClick={handleExcel} disabled={!summary || !!exporting || loading}>
            <FileSpreadsheet className="h-4 w-4" /> {exporting === 'xlsx' ? L.exporting : L.exportExcel}
          </Button>
          <Button variant="outline" className="gap-2" onClick={handlePdf} disabled={!summary || !!exporting || loading}>
            {exporting === 'pdf' ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
            {exporting === 'pdf' ? L.exporting : L.exportPdf}
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-6">
            {isAdmin && (
              <FilterSelect id="f-owner" label={L.doctor} value={filters.owner_id ?? ''} onChange={(v) => setFilter('owner_id', v)}>
                <option value="">{L.all}</option>
                {doctors.map((d) => <option key={d.id} value={d.id}>{d.full_name}</option>)}
              </FilterSelect>
            )}
            <FilterSelect id="f-genero" label={L.gender} value={filters.genero ?? ''} onChange={(v) => setFilter('genero', v)}>
              <option value="">{L.all}</option>
              {options?.genero.map((g) => <option key={g} value={g}>{g}</option>)}
            </FilterSelect>
            <FilterSelect id="f-causa" label={L.cause} value={filters.causa ?? ''} onChange={(v) => setFilter('causa', v)}>
              <option value="">{L.allF}</option>
              {options?.cause.map((c) => <option key={c} value={c}>{c}</option>)}
            </FilterSelect>
            <FilterSelect id="f-perfil" label={L.profile} value={filters.perfil ?? ''} onChange={(v) => setFilter('perfil', v)}>
              <option value="">{L.all}</option>
              {options?.profile.map((p) => <option key={p} value={p}>Perfil {p}</option>)}
            </FilterSelect>
            <div className="space-y-1">
              <label htmlFor="f-edad-min" className="text-xs font-medium text-muted-foreground">{L.ageFrom}</label>
              <input id="f-edad-min" type="number" min={0} max={120} value={filters.edad_min ?? ''}
                     onChange={(e) => setFilter('edad_min', e.target.value, false)}
                     className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm" />
            </div>
            <div className="space-y-1">
              <label htmlFor="f-edad-max" className="text-xs font-medium text-muted-foreground">{L.ageTo}</label>
              <input id="f-edad-max" type="number" min={0} max={120} value={filters.edad_max ?? ''}
                     onChange={(e) => setFilter('edad_max', e.target.value, false)}
                     className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm" />
            </div>
          </div>
          {hasFilters && (
            <Button variant="ghost" size="sm" className="mt-3" onClick={clear}>{L.clearFilters}</Button>
          )}
        </CardContent>
      </Card>

      {error ? (
        <Card>
          <CardContent className="p-6 flex items-center justify-between gap-4" role="alert">
            <p className="text-destructive">{L.loadError}: {error}</p>
            <Button variant="outline" className="gap-2" onClick={() => load(applied)}><RefreshCw className="h-4 w-4" /> {L.retry}</Button>
          </CardContent>
        </Card>
      ) : loading && !summary ? (
        <div className="flex items-center justify-center min-h-[300px]" aria-busy="true">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          <span className="sr-only">{L.loading}</span>
        </div>
      ) : summary && charts ? (
        <div className={loading ? 'opacity-60 transition-opacity' : 'transition-opacity'}>
          <p className="text-xs text-muted-foreground mb-3">
            {summary.scope === 'global' ? L.scopeGlobal : L.scopeOwn} · {L.generatedAt}: {new Date(summary.generated_at).toLocaleString(lang === 'en' ? 'en-US' : 'es-CO')}
          </p>
          <Tabs defaultValue="patients">
            <TabsList>
              <TabsTrigger value="patients">{L.tabPatients}</TabsTrigger>
              <TabsTrigger value="icf">{L.tabIcf}</TabsTrigger>
            </TabsList>

            <TabsContent value="patients" className="space-y-6">
              <div className="grid gap-4 grid-cols-2 lg:grid-cols-5">
                <Kpi testId="kpi-patients" label={L.kpiPatients} value={summary.totals.patients} />
                <Kpi testId="kpi-prediction" label={L.kpiPrediction} value={summary.totals.with_prediction} />
                <Kpi testId="kpi-prediction-rate" label={L.kpiPredictionRate} value={formatPercent(summary.totals.prediction_rate)} />
                <Kpi testId="kpi-mean-age" label={L.kpiMeanAge} value={formatNumber(summary.totals.mean_age)} />
                <Kpi testId="kpi-mean-global" label={L.kpiMeanGlobal} value={formatNumber(summary.totals.mean_global_level)} />
              </div>
              {summary.totals.patients === 0 ? (
                <Card><CardContent className="p-6 text-muted-foreground" data-testid="empty-patients">{L.empty}</CardContent></Card>
              ) : renderGrid(charts.patients)}
            </TabsContent>

            <TabsContent value="icf" className="space-y-6">
              <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
                <Kpi testId="kpi-with-icf" label={L.kpiWithIcf} value={summary.totals.with_icf_profile} />
                <Kpi testId="kpi-suggestions" label={L.kpiSuggestions} value={summary.icf.suggestions} />
                <Kpi testId="kpi-decided" label={L.kpiDecided} value={summary.icf.decided} />
                <Kpi testId="kpi-acceptance" label={L.kpiAcceptance} value={formatPercent(summary.icf.acceptance_rate)} help={L.kpiAcceptanceHelp} />
              </div>
              {summary.icf.suggestions === 0 ? (
                <Card><CardContent className="p-6 text-muted-foreground" data-testid="empty-icf">{L.emptyIcf}</CardContent></Card>
              ) : (
                <>
                  {renderGrid(charts.icf)}
                  <Card>
                    <CardHeader><CardTitle className="text-base">{L.chTopCodes}</CardTitle></CardHeader>
                    <CardContent>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>{L.colCode}</TableHead><TableHead>{L.colTitle}</TableHead><TableHead>{L.colComponent}</TableHead>
                            <TableHead className="text-right">{L.colCount}</TableHead>
                            <TableHead className="text-right">{L.colAccepted}</TableHead>
                            <TableHead className="text-right">{L.colRejected}</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {summary.icf.top_codes.map((c) => (
                            <TableRow key={c.code}>
                              <TableCell className="font-mono">{c.code}</TableCell>
                              <TableCell>{c.title}</TableCell>
                              <TableCell>{L[c.component]}</TableCell>
                              <TableCell className="text-right">{c.count}</TableCell>
                              <TableCell className="text-right">{c.accepted}</TableCell>
                              <TableCell className="text-right">{c.rejected}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </CardContent>
                  </Card>
                </>
              )}
            </TabsContent>
          </Tabs>

          {offscreen && (
            <div ref={offscreenRef} aria-hidden="true" style={{ position: 'absolute', left: -10000, top: 0 }}>
              {[...charts.patients, ...charts.icf]
                .filter((c) => summary.totals.patients > 0 && (c.id !== 'status' && c.id !== 'origin' && c.id !== 'model' ? true : summary.icf.suggestions > 0))
                .map((c) => (
                  <div key={c.id} data-chart-title={c.title} data-chart-note={c.note}>{c.render({ width: 520, height: c.id === 'cause' ? 360 : 300 })}</div>
                ))}
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}
