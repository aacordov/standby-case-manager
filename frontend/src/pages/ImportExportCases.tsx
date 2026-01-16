import { useState } from 'react';
import { Upload, Download, FileSpreadsheet, AlertCircle, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useToast } from '../context/ToastContext';
import api from '../api/axios';

interface ImportResult {
    message: string;
    casos_importados: number;
    casos_actualizados: number;
    observaciones_importadas: number;
    errores_casos: string[];
    errores_observaciones: string[];
}

export default function ImportExportCases() {
    const [casosFile, setCasosFile] = useState<File | null>(null);
    const [observacionesFile, setObservacionesFile] = useState<File | null>(null);
    const [isImporting, setIsImporting] = useState(false);
    const [isExporting, setIsExporting] = useState(false);
    const [importResult, setImportResult] = useState<ImportResult | null>(null);
    const { showToast } = useToast();

    const handleCasosFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setCasosFile(e.target.files[0]);
            setImportResult(null);
        }
    };

    const handleObservacionesFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setObservacionesFile(e.target.files[0]);
        }
    };

    const handleImport = async () => {
        if (!casosFile) {
            showToast('Por favor selecciona el archivo de casos', 'error');
            return;
        }

        setIsImporting(true);
        setImportResult(null);

        try {
            const formData = new FormData();
            formData.append('casos_file', casosFile);
            
            if (observacionesFile) {
                formData.append('observaciones_file', observacionesFile);
            }

            const response = await api.post('/cases-io/import-with-observations', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setImportResult(response.data);
            
            const hasErrors = response.data.errores_casos.length > 0 || 
                             response.data.errores_observaciones.length > 0;

            if (hasErrors) {
                showToast('Importación completada con algunos errores', 'warning');
            } else {
                showToast('Importación completada exitosamente', 'success');
            }

            // Limpiar archivos después de importación exitosa
            setCasosFile(null);
            setObservacionesFile(null);
            
            // Limpiar inputs de archivos
            const casosInput = document.getElementById('casos-file') as HTMLInputElement;
            const obsInput = document.getElementById('observaciones-file') as HTMLInputElement;
            if (casosInput) casosInput.value = '';
            if (obsInput) obsInput.value = '';

        } catch (error: any) {
            console.error('Error importing cases:', error);
            showToast(
                error.response?.data?.detail || 'Error al importar casos',
                'error'
            );
        } finally {
            setIsImporting(false);
        }
    };

    const handleExport = async (format: 'xlsx' | 'csv' = 'xlsx') => {
        setIsExporting(true);
        
        try {
            const response = await api.get(`/cases-io/export-with-observations?format=${format}`, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `casos_y_observaciones_export.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);
            window.URL.revokeObjectURL(url);

            showToast('Exportación completada exitosamente', 'success');
        } catch (error) {
            console.error('Error exporting cases:', error);
            showToast('Error al exportar casos', 'error');
        } finally {
            setIsExporting(false);
        }
    };

    const handleExportSimple = async (format: 'tsv' | 'csv' | 'xlsx' = 'xlsx') => {
        setIsExporting(true);
        
        try {
            const response = await api.get(`/cases-io/export?format=${format}`, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `casos_export.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);
            window.URL.revokeObjectURL(url);

            showToast('Exportación simple completada', 'success');
        } catch (error) {
            console.error('Error exporting cases:', error);
            showToast('Error al exportar casos', 'error');
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="border-b border-slate-200 dark:border-slate-700 pb-4">
                <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                    Importar / Exportar Casos
                </h1>
                <p className="text-slate-600 dark:text-slate-400 mt-1">
                    Gestiona la importación y exportación masiva de casos y observaciones
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* SECCIÓN DE IMPORTACIÓN */}
                <Card>
                    <div className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                                <Upload className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                            </div>
                            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                                Importar Casos
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {/* Archivo de Casos */}
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Archivo de Casos (Requerido) *
                                </label>
                                <div className="relative">
                                    <input
                                        id="casos-file"
                                        type="file"
                                        accept=".xlsx,.xls"
                                        onChange={handleCasosFileChange}
                                        className="block w-full text-sm text-slate-500 dark:text-slate-400
                                            file:mr-4 file:py-2 file:px-4
                                            file:rounded-lg file:border-0
                                            file:text-sm file:font-semibold
                                            file:bg-blue-50 file:text-blue-700
                                            hover:file:bg-blue-100
                                            dark:file:bg-blue-900 dark:file:text-blue-300
                                            dark:hover:file:bg-blue-800
                                            cursor-pointer"
                                    />
                                </div>
                                {casosFile && (
                                    <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2">
                                        <FileSpreadsheet className="h-4 w-4" />
                                        {casosFile.name}
                                    </p>
                                )}
                            </div>

                            {/* Archivo de Observaciones */}
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Archivo de Observaciones (Opcional)
                                </label>
                                <div className="relative">
                                    <input
                                        id="observaciones-file"
                                        type="file"
                                        accept=".xlsx,.xls"
                                        onChange={handleObservacionesFileChange}
                                        className="block w-full text-sm text-slate-500 dark:text-slate-400
                                            file:mr-4 file:py-2 file:px-4
                                            file:rounded-lg file:border-0
                                            file:text-sm file:font-semibold
                                            file:bg-slate-50 file:text-slate-700
                                            hover:file:bg-slate-100
                                            dark:file:bg-slate-800 dark:file:text-slate-300
                                            dark:hover:file:bg-slate-700
                                            cursor-pointer"
                                    />
                                </div>
                                {observacionesFile && (
                                    <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2">
                                        <FileSpreadsheet className="h-4 w-4" />
                                        {observacionesFile.name}
                                    </p>
                                )}
                            </div>

                            {/* Botón de Importar */}
                            <Button
                                onClick={handleImport}
                                disabled={!casosFile || isImporting}
                                className="w-full"
                            >
                                {isImporting ? (
                                    <>
                                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        Importando...
                                    </>
                                ) : (
                                    <>
                                        <Upload className="h-4 w-4 mr-2" />
                                        Importar Casos
                                    </>
                                )}
                            </Button>

                            {/* Información de ayuda */}
                            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
                                <div className="flex gap-2">
                                    <AlertCircle className="h-5 w-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                                    <div className="text-sm text-blue-800 dark:text-blue-300">
                                        <p className="font-medium mb-1">Formato de archivos:</p>
                                        <ul className="list-disc list-inside space-y-1 text-xs">
                                            <li>Casos: codigo, servicio_o_plataforma, estado, prioridad</li>
                                            <li>Observaciones: case_codigo, content, created_at</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </Card>

                {/* SECCIÓN DE EXPORTACIÓN */}
                <Card>
                    <div className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="p-2 bg-emerald-100 dark:bg-emerald-900 rounded-lg">
                                <Download className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                            </div>
                            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                                Exportar Casos
                            </h2>
                        </div>

                        <div className="space-y-4">
                            {/* Exportar con Observaciones */}
                            <div>
                                <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">
                                    Exportación Completa (Casos + Observaciones)
                                </h3>
                                <div className="flex gap-2">
                                    <Button
                                        onClick={() => handleExport('xlsx')}
                                        disabled={isExporting}
                                        variant="outline"
                                        className="flex-1"
                                    >
                                        {isExporting ? (
                                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        ) : (
                                            <Download className="h-4 w-4 mr-2" />
                                        )}
                                        Excel
                                    </Button>
                                    <Button
                                        onClick={() => handleExport('csv')}
                                        disabled={isExporting}
                                        variant="outline"
                                        className="flex-1"
                                    >
                                        {isExporting ? (
                                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        ) : (
                                            <Download className="h-4 w-4 mr-2" />
                                        )}
                                        CSV
                                    </Button>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                                    Exporta casos y observaciones en hojas separadas
                                </p>
                            </div>

                            <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
                                <h3 className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">
                                    Exportación Simple (Solo Casos)
                                </h3>
                                <div className="flex gap-2">
                                    <Button
                                        onClick={() => handleExportSimple('xlsx')}
                                        disabled={isExporting}
                                        variant="secondary"
                                        className="flex-1"
                                    >
                                        Excel
                                    </Button>
                                    <Button
                                        onClick={() => handleExportSimple('csv')}
                                        disabled={isExporting}
                                        variant="secondary"
                                        className="flex-1"
                                    >
                                        CSV
                                    </Button>
                                    <Button
                                        onClick={() => handleExportSimple('tsv')}
                                        disabled={isExporting}
                                        variant="secondary"
                                        className="flex-1"
                                    >
                                        TSV
                                    </Button>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                                    Exporta solo la información de casos
                                </p>
                            </div>

                            {/* Información de exportación */}
                            <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg p-3">
                                <div className="flex gap-2">
                                    <AlertCircle className="h-5 w-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" />
                                    <div className="text-sm text-emerald-800 dark:text-emerald-300">
                                        <p className="font-medium mb-1">Contenido exportado:</p>
                                        <ul className="list-disc list-inside space-y-1 text-xs">
                                            <li>Excel: 2 hojas (Casos + Observaciones)</li>
                                            <li>CSV: Solo tabla de casos</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </Card>
            </div>

            {/* RESULTADO DE IMPORTACIÓN */}
            {importResult && (
                <Card>
                    <div className="p-6">
                        <div className="flex items-center gap-3 mb-4">
                            {importResult.errores_casos.length === 0 && 
                             importResult.errores_observaciones.length === 0 ? (
                                <CheckCircle className="h-6 w-6 text-emerald-600 dark:text-emerald-400" />
                            ) : (
                                <AlertCircle className="h-6 w-6 text-amber-600 dark:text-amber-400" />
                            )}
                            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                                Resultado de Importación
                            </h3>
                        </div>

                        {/* Estadísticas */}
                        <div className="grid grid-cols-3 gap-4 mb-4">
                            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 text-center">
                                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                                    {importResult.casos_importados}
                                </p>
                                <p className="text-sm text-slate-600 dark:text-slate-400">
                                    Casos Importados
                                </p>
                            </div>
                            <div className="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4 text-center">
                                <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">
                                    {importResult.casos_actualizados}
                                </p>
                                <p className="text-sm text-slate-600 dark:text-slate-400">
                                    Casos Actualizados
                                </p>
                            </div>
                            <div className="bg-emerald-50 dark:bg-emerald-900/20 rounded-lg p-4 text-center">
                                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                                    {importResult.observaciones_importadas}
                                </p>
                                <p className="text-sm text-slate-600 dark:text-slate-400">
                                    Observaciones Importadas
                                </p>
                            </div>
                        </div>

                        {/* Errores */}
                        {(importResult.errores_casos.length > 0 || 
                          importResult.errores_observaciones.length > 0) && (
                            <div className="space-y-3">
                                {importResult.errores_casos.length > 0 && (
                                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
                                        <div className="flex items-start gap-2">
                                            <XCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                                            <div className="flex-1">
                                                <p className="text-sm font-medium text-red-800 dark:text-red-300 mb-2">
                                                    Errores en Casos ({importResult.errores_casos.length}):
                                                </p>
                                                <ul className="text-xs text-red-700 dark:text-red-400 space-y-1 max-h-32 overflow-y-auto">
                                                    {importResult.errores_casos.map((error, idx) => (
                                                        <li key={idx}>• {error}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {importResult.errores_observaciones.length > 0 && (
                                    <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-3">
                                        <div className="flex items-start gap-2">
                                            <AlertCircle className="h-5 w-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                                            <div className="flex-1">
                                                <p className="text-sm font-medium text-amber-800 dark:text-amber-300 mb-2">
                                                    Errores en Observaciones ({importResult.errores_observaciones.length}):
                                                </p>
                                                <ul className="text-xs text-amber-700 dark:text-amber-400 space-y-1 max-h-32 overflow-y-auto">
                                                    {importResult.errores_observaciones.map((error, idx) => (
                                                        <li key={idx}>• {error}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </Card>
            )}
        </div>
    );
}
