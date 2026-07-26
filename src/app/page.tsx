'use client';

import React, { useState, useEffect, useMemo } from 'react';
import {
  Card, CardContent, CardDescription, CardHeader, CardTitle,
} from '@/components/ui/card';
import {
  Tabs, TabsContent, TabsList, TabsTrigger,
} from '@/components/ui/tabs';
import {
  Badge,
} from '@/components/ui/badge';
import {
  Button,
} from '@/components/ui/button';
import {
  Input,
} from '@/components/ui/input';
import {
  Progress,
} from '@/components/ui/progress';
import {
  Accordion, AccordionContent, AccordionItem, AccordionTrigger,
} from '@/components/ui/accordion';
import {
  ScrollArea,
} from '@/components/ui/scroll-area';
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from '@/components/ui/dialog';
import {
  Separator,
} from '@/components/ui/separator';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import {
  Alert, AlertDescription, AlertTitle,
} from '@/components/ui/alert';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts';
import {
  Search, Copy, GitMerge, AlertTriangle, CheckCircle2, Lightbulb,
  Bot, MessageSquare, Mail, Video, ShoppingCart, Megaphone,
  Calendar, Mic, Database, FileText, Wrench, Layers,
  Filter, ChevronDown, ChevronUp, Brain, Workflow, Zap,
  ArrowRight, ExternalLink, TrendingUp, Package, Shield,
} from 'lucide-react';

interface Workflow {
  id: string;
  name: string;
  file_path: string;
  file_name: string;
  source: string;
  folder_category: string;
  node_count: number;
  connection_count: number;
  node_types: string[];
  node_names: string[];
  categories: string[];
  tags: string[];
  active: boolean;
  descriptions: string[];
}

interface Duplication {
  workflow_1: string;
  workflow_2: string;
  name_1: string;
  name_2: string;
  similarity: number;
  type: string;
  reason: string;
}

interface Similarity {
  workflow_1: string;
  workflow_2: string;
  name_1: string;
  name_2: string;
  similarity: number;
  type: string;
  reason: string;
}

interface ConsolidationSuggestion {
  group_name: string;
  workflows: { id: string; name: string; source: string; node_count: number }[];
  similarity: number;
  type: string;
  suggestion: string;
  categories: string[];
}

interface BestPractices {
  good: { title: string; description: string; impact: string }[];
  warnings: { title: string; description: string; impact: string }[];
  recommendations: { title: string; description: string; impact: string }[];
}

interface Stats {
  total_workflows: number;
  total_node_types: number;
  avg_node_count: number;
  max_node_count: number;
  min_node_count: number;
  duplications_count: number;
  similarities_count: number;
  categories_distribution: Record<string, number>;
  sources_distribution: Record<string, number>;
  node_type_frequency: Record<string, number>;
  top_node_types: { type: string; count: number }[];
}

interface CatalogData {
  metadata: { analysis_date: string; total_files_analyzed: number; total_workflows_parsed: number; parse_errors: number };
  stats: Stats;
  workflows: Workflow[];
  catalog_by_category: Record<string, Workflow[]>;
  duplications: Duplication[];
  similarities: Similarity[];
  consolidation_suggestions: ConsolidationSuggestion[];
  best_practices: BestPractices;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  'IA & Agentes': <Brain className="w-4 h-4" />,
  'Chat & Mensajería': <MessageSquare className="w-4 h-4" />,
  'Email & Comunicación': <Mail className="w-4 h-4" />,
  'Social Media & Contenido': <Video className="w-4 h-4" />,
  'Marketing & Leads': <Megaphone className="w-4 h-4" />,
  'Voz & Transcripción': <Mic className="w-4 h-4" />,
  'MCP Tools': <Wrench className="w-4 h-4" />,
  'Scraping & Extracción': <Filter className="w-4 h-4" />,
  'Calendario & Agenda': <Calendar className="w-4 h-4" />,
  'RRHH & Selección': <FileText className="w-4 h-4" />,
  'Base de Datos': <Database className="w-4 h-4" />,
  'RAG & Vector Store': <Layers className="w-4 h-4" />,
  'E-Commerce & Ventas': <ShoppingCart className="w-4 h-4" />,
  'Dashboard & Datos': <TrendingUp className="w-4 h-4" />,
  'Utilidades & DevOps': <Shield className="w-4 h-4" />,
  'Flowise Integration': <Workflow className="w-4 h-4" />,
  'Documentos & PDF': <FileText className="w-4 h-4" />,
  'General': <Package className="w-4 h-4" />,
};

const CATEGORY_COLORS: Record<string, string> = {
  'IA & Agentes': '#8b5cf6',
  'Chat & Mensajería': '#06b6d4',
  'Email & Comunicación': '#f59e0b',
  'Social Media & Contenido': '#ec4899',
  'Marketing & Leads': '#10b981',
  'Voz & Transcripción': '#6366f1',
  'MCP Tools': '#f97316',
  'Scraping & Extracción': '#14b8a6',
  'Calendario & Agenda': '#0ea5e9',
  'RRHH & Selección': '#a855f7',
  'Base de Datos': '#22c55e',
  'RAG & Vector Store': '#e11d48',
  'E-Commerce & Ventas': '#f43f5e',
  'Dashboard & Datos': '#84cc16',
  'Utilidades & DevOps': '#64748b',
  'Flowise Integration': '#d946ef',
  'Documentos & PDF': '#78716c',
  'General': '#94a3b8',
};

const IMPACT_COLORS: Record<string, string> = {
  critical: 'bg-red-100 text-red-800 border-red-300',
  high: 'bg-orange-100 text-orange-800 border-orange-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  low: 'bg-green-100 text-green-800 border-green-300',
};

function formatNodeType(type: string): string {
  if (type.startsWith('@n8n/n8n-nodes-langchain.')) {
    const name = type.replace('@n8n/n8n-nodes-langchain.', '');
    return `LangChain: ${name}`;
  }
  if (type.startsWith('n8n-nodes-base.')) {
    return type.replace('n8n-nodes-base.', '');
  }
  return type;
}

export default function CatalogPage() {
  const [data, setData] = useState<CatalogData | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedSource, setSelectedSource] = useState<string>('all');
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);
  const [activeTab, setActiveTab] = useState('catalog');
  const [expandedSuggestions, setExpandedSuggestions] = useState<Set<number>>(new Set());

  useEffect(() => {
    fetch('/api/catalog')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const filteredWorkflows = useMemo(() => {
    if (!data) return [];
    let wfs = data.workflows;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      wfs = wfs.filter(w =>
        w.name.toLowerCase().includes(term) ||
        w.categories.some(c => c.toLowerCase().includes(term)) ||
        w.node_types.some(t => t.toLowerCase().includes(term)) ||
        w.source.toLowerCase().includes(term)
      );
    }
    if (selectedCategory !== 'all') {
      wfs = wfs.filter(w => w.categories.includes(selectedCategory));
    }
    if (selectedSource !== 'all') {
      wfs = wfs.filter(w => w.source === selectedSource);
    }
    return wfs;
  }, [data, searchTerm, selectedCategory, selectedSource]);

  const categoryChartData = useMemo(() => {
    if (!data) return [];
    return Object.entries(data.stats.categories_distribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 12)
      .map(([name, value]) => ({
        name,
        value,
        fill: CATEGORY_COLORS[name] || '#94a3b8',
      }));
  }, [data]);

  const sourceChartData = useMemo(() => {
    if (!data) return [];
    return Object.entries(data.stats.sources_distribution)
      .sort((a, b) => b[1] - a[1])
      .map(([name, value]) => ({ name, value }));
  }, [data]);

  const nodeTypeChartData = useMemo(() => {
    if (!data) return [];
    return data.stats.top_node_types.slice(0, 10).map(item => ({
      name: formatNodeType(item.type),
      count: item.count,
    }));
  }, [data]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 rounded-full border-4 border-violet-200 border-t-violet-600 animate-spin" />
          <p className="text-slate-600 text-lg font-medium">Analizando automatizaciones...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <Alert variant="destructive" className="max-w-md">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>No se pudo cargar los datos del catálogo.</AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg">
                <Workflow className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
                  Catálogo de Automatizaciones n8n
                </h1>
                <p className="text-sm text-slate-500">
                  {data.stats.total_workflows} workflows analizados &middot; {data.stats.duplications_count} duplicaciones &middot; {data.stats.similarities_count} similitudes
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <div className="relative w-full sm:w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <Input
                  placeholder="Buscar workflows..."
                  value={searchTerm}
                  onChange={e => setSearchTerm(e.target.value)}
                  className="pl-9 h-9"
                />
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-white shadow-sm border border-slate-200 h-auto p-1 grid grid-cols-2 sm:grid-cols-5 gap-1">
            <TabsTrigger value="overview" className="flex items-center gap-1.5 data-[state=active]:bg-violet-600 data-[state=active]:text-white text-xs sm:text-sm px-3 py-2">
              <TrendingUp className="w-4 h-4" />
              <span className="hidden sm:inline">Resumen</span>
            </TabsTrigger>
            <TabsTrigger value="catalog" className="flex items-center gap-1.5 data-[state=active]:bg-violet-600 data-[state=active]:text-white text-xs sm:text-sm px-3 py-2">
              <Package className="w-4 h-4" />
              <span className="hidden sm:inline">Catálogo</span>
            </TabsTrigger>
            <TabsTrigger value="duplicates" className="flex items-center gap-1.5 data-[state=active]:bg-violet-600 data-[state=active]:text-white text-xs sm:text-sm px-3 py-2">
              <Copy className="w-4 h-4" />
              <span className="hidden sm:inline">Duplicados</span>
            </TabsTrigger>
            <TabsTrigger value="consolidation" className="flex items-center gap-1.5 data-[state=active]:bg-violet-600 data-[state=active]:text-white text-xs sm:text-sm px-3 py-2">
              <GitMerge className="w-4 h-4" />
              <span className="hidden sm:inline">Consolidación</span>
            </TabsTrigger>
            <TabsTrigger value="practices" className="flex items-center gap-1.5 data-[state=active]:bg-violet-600 data-[state=active]:text-white text-xs sm:text-sm px-3 py-2">
              <Lightbulb className="w-4 h-4" />
              <span className="hidden sm:inline">Prácticas</span>
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <Card className="bg-gradient-to-br from-violet-50 to-violet-100 border-violet-200">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-violet-600">Total Workflows</p>
                      <p className="text-3xl font-bold text-violet-900">{data.stats.total_workflows}</p>
                    </div>
                    <Workflow className="w-8 h-8 text-violet-400" />
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-gradient-to-br from-red-50 to-red-100 border-red-200">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-red-600">Duplicaciones</p>
                      <p className="text-3xl font-bold text-red-900">{data.stats.duplications_count}</p>
                    </div>
                    <Copy className="w-8 h-8 text-red-400" />
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-gradient-to-br from-amber-50 to-amber-100 border-amber-200">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-amber-600">Similitudes</p>
                      <p className="text-3xl font-bold text-amber-900">{data.stats.similarities_count}</p>
                    </div>
                    <GitMerge className="w-8 h-8 text-amber-400" />
                  </div>
                </CardContent>
              </Card>
              <Card className="bg-gradient-to-br from-emerald-50 to-emerald-100 border-emerald-200">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-emerald-600">Categorías</p>
                      <p className="text-3xl font-bold text-emerald-900">{Object.keys(data.stats.categories_distribution).length}</p>
                    </div>
                    <Layers className="w-8 h-8 text-emerald-400" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Node stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <Card>
                <CardContent className="pt-4 pb-4">
                  <p className="text-xs text-slate-500">Promedio nodos</p>
                  <p className="text-xl font-bold">{data.stats.avg_node_count}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4 pb-4">
                  <p className="text-xs text-slate-500">Max nodos</p>
                  <p className="text-xl font-bold">{data.stats.max_node_count}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4 pb-4">
                  <p className="text-xs text-slate-500">Min nodos</p>
                  <p className="text-xl font-bold">{data.stats.min_node_count}</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="pt-4 pb-4">
                  <p className="text-xs text-slate-500">Tipos de nodos únicos</p>
                  <p className="text-xl font-bold">{data.stats.total_node_types}</p>
                </CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Distribución por Categoría</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={350}>
                    <BarChart data={categoryChartData} layout="vertical">
                      <XAxis type="number" />
                      <YAxis dataKey="name" type="category" width={140} tick={{ fontSize: 11 }} />
                      <Tooltip />
                      <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                        {categoryChartData.map((entry, idx) => (
                          <Cell key={idx} fill={entry.fill} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Distribución por Fuente</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={350}>
                    <PieChart>
                      <Pie
                        data={sourceChartData}
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        innerRadius={60}
                        dataKey="value"
                        nameKey="name"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {sourceChartData.map((_, idx) => (
                          <Cell key={idx} fill={['#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ec4899', '#64748b'][idx % 6]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Top Node Types */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Top 10 Tipos de Nodos Más Usados</CardTitle>
                <CardDescription>Los nodos que aparecen con mayor frecuencia en todos los workflows</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={nodeTypeChartData}>
                    <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-30} textAnchor="end" height={80} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Catalog Tab */}
          <TabsContent value="catalog" className="space-y-4">
            {/* Filters */}
            <div className="flex flex-wrap gap-3 items-center">
              <Select value={selectedCategory} onValueChange={v => setSelectedCategory(v)}>
                <SelectTrigger className="w-[200px] h-9">
                  <SelectValue placeholder="Categoría" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas las categorías</SelectItem>
                  {Object.keys(data.stats.categories_distribution).sort().map(cat => (
                    <SelectItem key={cat} value={cat}>{cat} ({data.stats.categories_distribution[cat]})</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select value={selectedSource} onValueChange={v => setSelectedSource(v)}>
                <SelectTrigger className="w-[200px] h-9">
                  <SelectValue placeholder="Fuente" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todas las fuentes</SelectItem>
                  {Object.keys(data.stats.sources_distribution).sort().map(src => (
                    <SelectItem key={src} value={src}>{src} ({data.stats.sources_distribution[src]})</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Badge variant="outline" className="h-9 px-3">
                {filteredWorkflows.length} resultados
              </Badge>
            </div>

            {/* Workflow Cards */}
            <ScrollArea className="h-[calc(100vh-260px)]">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 pr-4 pb-4">
                {filteredWorkflows.map(wf => (
                  <Card
                    key={wf.id}
                    className="hover:shadow-lg transition-all duration-200 cursor-pointer group border-slate-200 hover:border-violet-300"
                    onClick={() => setSelectedWorkflow(wf)}
                  >
                    <CardHeader className="pb-2">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-sm font-semibold line-clamp-2 group-hover:text-violet-700 transition-colors">
                          {wf.name}
                        </CardTitle>
                        <div className="flex items-center gap-1 text-xs text-slate-400 shrink-0">
                          <Zap className="w-3 h-3" />
                          {wf.node_count}
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0 pb-4">
                      <div className="flex flex-wrap gap-1 mb-2">
                        {wf.categories.slice(0, 3).map(cat => (
                          <Badge
                            key={cat}
                            variant="secondary"
                            className="text-xs px-1.5 py-0.5"
                            style={{ backgroundColor: CATEGORY_COLORS[cat] + '20', color: CATEGORY_COLORS[cat], borderColor: CATEGORY_COLORS[cat] + '40' }}
                          >
                            <span className="flex items-center gap-1">
                              {CATEGORY_ICONS[cat]}
                              {cat}
                            </span>
                          </Badge>
                        ))}
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500">
                        <span className="truncate max-w-[180px]">{wf.source}</span>
                        <span>{wf.connection_count} conexiones</span>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-1">
                        {wf.node_types.slice(0, 4).map(nt => (
                          <Badge key={nt} variant="outline" className="text-xs px-1 py-0">
                            {formatNodeType(nt)}
                          </Badge>
                        ))}
                        {wf.node_types.length > 4 && (
                          <Badge variant="outline" className="text-xs px-1 py-0 text-slate-400">
                            +{wf.node_types.length - 4}
                          </Badge>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </ScrollArea>
          </TabsContent>

          {/* Duplicates Tab */}
          <TabsContent value="duplicates" className="space-y-6">
            <Alert className="border-red-300 bg-red-50">
              <AlertTriangle className="h-4 w-4 text-red-600" />
              <AlertTitle className="text-red-800">Atención: Duplicaciones Detectadas</AlertTitle>
              <AlertDescription className="text-red-700">
                Se encontraron {data.stats.duplications_count} workflows duplicados y {data.stats.similarities_count} similitudes.
                Las duplicaciones generan mantenimiento redundante, inconsistencias y mayor riesgo de errores.
              </AlertDescription>
            </Alert>

            {/* Exact Duplicates */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Copy className="w-5 h-5 text-red-500" />
                  Duplicaciones Exactas ({data.duplications.filter(d => d.similarity >= 90).length})
                </CardTitle>
                <CardDescription>Workflows con similitud ≥ 90% — prácticamente idénticos</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="max-h-[400px]">
                  <div className="space-y-3">
                    {data.duplications.filter(d => d.similarity >= 90).map((d, idx) => (
                      <div key={idx} className="p-3 rounded-lg border border-red-200 bg-red-50/50">
                        <div className="flex items-center justify-between mb-2">
                          <Badge className="bg-red-600 text-white text-xs">Duplicado</Badge>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-red-700">{d.similarity}%</span>
                            <Progress value={d.similarity} className="w-24 h-2" />
                          </div>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          <div className="p-2 rounded bg-white border border-slate-200">
                            <p className="text-sm font-medium truncate">{d.name_1}</p>
                            <p className="text-xs text-slate-500 mt-1">{d.reason}</p>
                          </div>
                          <div className="p-2 rounded bg-white border border-slate-200">
                            <p className="text-sm font-medium truncate">{d.name_2}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          <ArrowRight className="w-4 h-4 text-violet-500" />
                          <span className="text-xs text-slate-600">Consolidar en un workflow único y parametrizable</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Similar Workflows */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <GitMerge className="w-5 h-5 text-amber-500" />
                  Workflows Similares ({data.similarities.length})
                </CardTitle>
                <CardDescription>Workflows con funcionalidad similar que podrían consolidarse</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="max-h-[400px]">
                  <div className="space-y-3">
                    {data.similarities.map((s, idx) => (
                      <div key={idx} className="p-3 rounded-lg border border-amber-200 bg-amber-50/50">
                        <div className="flex items-center justify-between mb-2">
                          <Badge className="bg-amber-600 text-white text-xs">Similar</Badge>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-amber-700">{s.similarity}%</span>
                            <Progress value={s.similarity} className="w-24 h-2" />
                          </div>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          <div className="p-2 rounded bg-white border border-slate-200">
                            <p className="text-sm font-medium truncate">{s.name_1}</p>
                          </div>
                          <div className="p-2 rounded bg-white border border-slate-200">
                            <p className="text-sm font-medium truncate">{s.name_2}</p>
                          </div>
                        </div>
                        <p className="text-xs text-slate-600 mt-2">{s.reason}</p>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Consolidation Tab */}
          <TabsContent value="consolidation" className="space-y-6">
            <Alert className="border-violet-300 bg-violet-50">
              <GitMerge className="h-4 w-4 text-violet-600" />
              <AlertTitle className="text-violet-800">Sugerencias de Consolidación</AlertTitle>
              <AlertDescription className="text-violet-700">
                Se identificaron {data.consolidation_suggestions.length} grupos de workflows que pueden consolidarse
                para reducir duplicación, mejorar mantenibilidad y estandarizar procesos.
              </AlertDescription>
            </Alert>

            <ScrollArea className="h-[calc(100vh-280px)]">
              <Accordion type="multiple" className="space-y-2 pr-4">
                {data.consolidation_suggestions.slice(0, 30).map((sug, idx) => (
                  <AccordionItem key={idx} value={`suggestion-${idx}`} className="border border-slate-200 rounded-lg bg-white">
                    <AccordionTrigger className="px-4 py-3 hover:no-underline hover:bg-slate-50">
                      <div className="flex items-center gap-3 flex-1">
                        <div className="w-8 h-8 rounded-lg bg-violet-100 flex items-center justify-center">
                          <GitMerge className="w-4 h-4 text-violet-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate capitalize">{sug.group_name}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="outline" className="text-xs">
                              {sug.type === 'duplicate' ? 'Duplicado' : 'Similar'}
                            </Badge>
                            <span className="text-xs text-slate-500">{sug.similarity}% similitud</span>
                            {sug.categories.map(cat => (
                              <Badge key={cat} variant="secondary" className="text-xs px-1 py-0" style={{ backgroundColor: CATEGORY_COLORS[cat] + '20', color: CATEGORY_COLORS[cat] }}>
                                {cat}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="px-4 pb-4">
                      <div className="space-y-3">
                        <p className="text-sm text-slate-700">{sug.suggestion}</p>
                        <Separator />
                        <div className="space-y-2">
                          {sug.workflows.map(wf => (
                            <div key={wf.id} className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-200">
                              <div className="flex items-center gap-2 min-w-0">
                                <Workflow className="w-4 h-4 text-slate-400" />
                                <p className="text-sm truncate">{wf.name}</p>
                              </div>
                              <div className="flex items-center gap-2 text-xs text-slate-500 shrink-0">
                                <Badge variant="outline" className="text-xs">{wf.source}</Badge>
                                <span>{wf.node_count} nodos</span>
                              </div>
                            </div>
                          ))}
                        </div>
                        <div className="flex items-center gap-2 pt-2">
                          <Button variant="outline" size="sm" className="text-xs">
                            <CheckCircle2 className="w-3 h-3 mr-1" />
                            Ver Detalle
                          </Button>
                          <Button variant="default" size="sm" className="text-xs bg-violet-600 hover:bg-violet-700">
                            <GitMerge className="w-3 h-3 mr-1" />
                            Consolidar
                          </Button>
                        </div>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </ScrollArea>
          </TabsContent>

          {/* Best Practices Tab */}
          <TabsContent value="practices" className="space-y-6">
            {/* Good Practices */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  Buenas Prácticas Detectadas
                </CardTitle>
                <CardDescription>Prácticas positivas observadas en los workflows analizados</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.best_practices.good.map((p, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${IMPACT_COLORS[p.impact]}`}>
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-medium text-sm">{p.title}</h4>
                        <Badge variant="outline" className="text-xs capitalize">{p.impact}</Badge>
                      </div>
                      <p className="text-sm mt-1">{p.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Warnings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  Alertas y Anti-Patrónes
                </CardTitle>
                <CardDescription>Problemas detectados que requieren atención</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.best_practices.warnings.map((w, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${IMPACT_COLORS[w.impact]}`}>
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-medium text-sm">{w.title}</h4>
                        <Badge variant="outline" className="text-xs capitalize">{w.impact}</Badge>
                      </div>
                      <p className="text-sm mt-1">{w.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recommendations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Lightbulb className="w-5 h-5 text-violet-500" />
                  Recomendaciones de Mejora
                </CardTitle>
                <CardDescription>Acciones sugeridas para optimizar el catálogo de automatizaciones</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {data.best_practices.recommendations.map((r, idx) => (
                    <div key={idx} className={`p-4 rounded-lg border ${IMPACT_COLORS[r.impact]}`}>
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-medium text-sm">{r.title}</h4>
                        <Badge variant="outline" className="text-xs capitalize">{r.impact}</Badge>
                      </div>
                      <p className="text-sm mt-1">{r.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Workflow Detail Modal */}
      <Dialog open={selectedWorkflow !== null} onOpenChange={() => setSelectedWorkflow(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh]">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Workflow className="w-5 h-5 text-violet-600" />
              {selectedWorkflow?.name}
            </DialogTitle>
            <DialogDescription>
              Detalle completo del workflow
            </DialogDescription>
          </DialogHeader>
          {selectedWorkflow && (
            <ScrollArea className="max-h-[60vh] pr-4">
              <div className="space-y-4">
                {/* Categories */}
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Categorías</h4>
                  <div className="flex flex-wrap gap-1">
                    {selectedWorkflow.categories.map(cat => (
                      <Badge key={cat} style={{ backgroundColor: CATEGORY_COLORS[cat] + '20', color: CATEGORY_COLORS[cat], borderColor: CATEGORY_COLORS[cat] + '40' }}>
                        <span className="flex items-center gap-1">{CATEGORY_ICONS[cat]} {cat}</span>
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 rounded bg-slate-50 border">
                    <p className="text-xs text-slate-500">Nodos</p>
                    <p className="text-lg font-bold">{selectedWorkflow.node_count}</p>
                  </div>
                  <div className="p-3 rounded bg-slate-50 border">
                    <p className="text-xs text-slate-500">Conexiones</p>
                    <p className="text-lg font-bold">{selectedWorkflow.connection_count}</p>
                  </div>
                </div>

                {/* Source */}
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Fuente</h4>
                  <Badge variant="outline">{selectedWorkflow.source}</Badge>
                </div>

                {/* Node Types */}
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Tipos de Nodos ({selectedWorkflow.node_types.length})</h4>
                  <div className="flex flex-wrap gap-1">
                    {selectedWorkflow.node_types.map(nt => (
                      <Badge key={nt} variant="secondary" className="text-xs">
                        {formatNodeType(nt)}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Node Names */}
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Nombres de Nodos ({selectedWorkflow.node_names.length})</h4>
                  <div className="flex flex-wrap gap-1">
                    {selectedWorkflow.node_names.slice(0, 20).map(nn => (
                      <Badge key={nn} variant="outline" className="text-xs">{nn}</Badge>
                    ))}
                    {selectedWorkflow.node_names.length > 20 && (
                      <Badge variant="outline" className="text-xs text-slate-400">+{selectedWorkflow.node_names.length - 20}</Badge>
                    )}
                  </div>
                </div>

                {/* Descriptions */}
                {selectedWorkflow.descriptions.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-700 mb-2">Descripciones (Sticky Notes)</h4>
                    <div className="space-y-2">
                      {selectedWorkflow.descriptions.map((desc, idx) => (
                        <div key={idx} className="p-3 rounded bg-yellow-50 border border-yellow-200 text-sm">
                          {desc}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tags */}
                {selectedWorkflow.tags.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-slate-700 mb-2">Tags</h4>
                    <div className="flex flex-wrap gap-1">
                      {selectedWorkflow.tags.map(tag => (
                        <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* File */}
                <div>
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Archivo</h4>
                  <p className="text-xs text-slate-500 truncate">{selectedWorkflow.file_name}</p>
                </div>
              </div>
            </ScrollArea>
          )}
        </DialogContent>
      </Dialog>

      {/* Footer */}
      <footer className="mt-auto bg-white border-t border-slate-200 py-4 text-center">
        <p className="text-sm text-slate-500">
          Catálogo de Automatizaciones n8n &middot; Análisis generado el {data.metadata.analysis_date} &middot; {data.metadata.total_workflows_parsed} workflows de {data.metadata.total_files_analyzed} archivos
        </p>
      </footer>
    </div>
  );
}
