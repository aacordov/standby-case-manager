import { useState } from 'react';
import { Upload, Download, FileSpreadsheet, AlertCircle, CheckCircle, XCircle, Loader2, Users } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useToast } from '../context/ToastContext';
import { useQueryClient } from '@tanstack/react-query';
import api from '../api/axios';

interface ImportResult {
    message: string;
    casos_importados?: number;
    casos_actualizados?: number;
    observaciones_importadas?: number;
    usuarios_importados?: number;
    usuarios_actualizados?: number;
    errores?: string[];
    errores_casos?: string[];
    errores_observaciones?: string[];
    contraseñas_generadas?: Array<{email: string; nombre: string; password: string}>;
    advertencia?: string;
}

export default function ImportExportCases() {
    const [completeFile, setCompleteFile] = useState<File | null>(null);
    const [usersFile, setUsersFile] = useState<File | null>(null);
    const [isImporting, setIsImporting] = useState(false);
    const [isImportingUsers, setIsImportingUsers] = useState(false);
    const [isExporting, setIsExporting] = useState(false);
    const [isExportingUsers, setIsExportingUsers] = useState(false);
    const [importResult, setImportResult] = useState<ImportResult | null>(null);
    const [userImportResult, setUserImportResult] = useState<ImportResult | null>(null);
    const { showToast } = useToast();
    const queryClient = useQueryClient();

    const handleCompleteFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setCompleteFile(e.target.files[0]);
            setImportResult(null);
        }
    };

    const handleUsersFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setUsersFile(e.target.files[0]);
            setUserImportResult(null);
        }
    };

    const handleImportComplete = async () => {
        if (!completeFile) {
            showToast('error', 'Error', 'Por favor selecciona un archivo Excel');
            return;
        }

        setIsImporting(true);
        setImportResult(null);

        try {
            const formData = new FormData();
            formData.append('file', completeFile);

            const response = await api.post('/cases-io/import-complete-excel', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setImportResult(response.data);
            
            const hasErrors = (response.data.errores && response.data.errores.length > 0);

            if (hasErrors) {
                showToast('warning', 'Importación completada', 'Se completó la importación pero con algunos errores');
            } else {
                showToast('success', 'Éxito', 'Importación completada exitosamente');
            }

            // ✅ Invalidar cache de casos para que se actualice el dashboard
            queryClient.invalidateQueries({ queryKey: ['cases'] });
            queryClient.invalidateQueries({ queryKey: ['stats'] });

            setCompleteFile(null);
            const fileInput = document.getElementById('complete-file') as HTMLInputElement;
            if (fileInput) fileInput.value = '';

        } catch (error: any) {
            console.error('Error importing:', error);
            showToast(
                'error',
                'Error al importar',
                error.response?.data?.detail || 'Error al importar el archivo'
            );
        } finally {
            setIsImporting(false);
        }
    };

    const handleImportUsers = async () => {
        if (!usersFile) {
            showToast('error', 'Error', 'Por favor selecciona un archivo de usuarios');
            return;
        }

        setIsImportingUsers(true);
        setUserImportResult(null);

        try {
            const formData = new FormData();
            formData.append('file', usersFile);

            const response = await api.post('/cases-io/import-users', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setUserImportResult(response.data);
            
            const hasErrors = (response.data.errores && response.data.errores.length > 0);

            if (hasErrors) {
                showToast('warning', 'Importación completada', 'Se completó la importación de usuarios pero con algunos errores');
            } else {
                showToast('success', 'Éxito', 'Usuarios importados exitosamente');
            }

            // ✅ Invalidar cache de usuarios para que se actualice la lista
            queryClient.invalidateQueries({ queryKey: ['users'] });

            setUsersFile(null);
            const fileInput = document.getElementById('users-file') as HTMLInputElement;
            if (fileInput) fileInput.value = '';

        } catch (error: any) {
            console.error('Error importing users:', error);
            showToast(
                'error',
                'Error al importar usuarios',
                error.response?.data?.detail || 'Error al importar usuarios'
            );
        } finally {
            setIsImportingUsers(false);
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
            link.setAttribute('download', `casos_completos.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);

            showToast('success', 'Éxito', `Casos exportados en formato ${format.toUpperCase()}`);
        } catch (error: any) {
            console.error('Error exporting cases:', error);
            showToast('error', 'Error al exportar', error.response?.data?.detail || 'Error al exportar casos');
        } finally {
            setIsExporting(false);
        }
    };

    const handleExportUsers = async (format: 'xlsx' | 'csv' = 'xlsx') => {
        setIsExportingUsers(true);
        
        try {
            const response = await api.get(`/cases-io/export-users?format=${format}`, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `usuarios_export.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode?.removeChild(link);

            showToast('success', 'Éxito', `Usuarios exportados en formato ${format.toUpperCase()}`);
        } catch (error: any) {
            console.error('Error exporting users:', error);
            showToast('error', 'Error al exportar usuarios', error.response?.data?.detail || 'Error al exportar usuarios');
        } finally {
            setIsExportingUsers(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                    Importar / Exportar Datos
                </h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">
                    Gestiona la importación y exportación de casos, observaciones y usuarios
                </p>
            </div>

            {/* SECCIÓN: CASOS Y OBSERVACIONES */}
            <Card className="p-6">
                <div className="flex items-center gap-3 mb-6">
                    <FileSpreadsheet className="text-indigo-500" size={24} />
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                        Casos y Observaciones
                    </h2>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* EXPORTAR */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2">
                            <Download size={20} />
                            Exportar Casos
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                            Exporta todos los casos con sus observaciones en un único archivo Excel con dos hojas.
                        </p>
                        <div className="flex gap-2">
                            <Button
                                variant="outline"
                                onClick={() => handleExport('xlsx')}
                                disabled={isExporting}
                                className="flex-1"
                            >
                                {isExporting ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Exportando...
                                    </>
                                ) : (
                                    <>
                                        <Download size={16} />
                                        Exportar Excel
                                    </>
                                )}
                            </Button>
                            <Button
                                variant="outline"
                                onClick={() => handleExport('csv')}
                                disabled={isExporting}
                                className="flex-1"
                            >
                                {isExporting ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Exportando...
                                    </>
                                ) : (
                                    <>
                                        <Download size={16} />
                                        Exportar CSV
                                    </>
                                )}
                            </Button>
                        </div>
                    </div>

                    {/* IMPORTAR */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2">
                            <Upload size={20} />
                            Importar Casos
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                            Importa casos y observaciones desde un archivo Excel con hojas "Casos" y "Observaciones".
                        </p>

                        <div className="space-y-3">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Archivo Excel Completo
                                </label>
                                <input
                                    id="complete-file"
                                    type="file"
                                    accept=".xlsx,.xls"
                                    onChange={handleCompleteFileChange}
                                    className="block w-full text-sm text-slate-500 dark:text-slate-400
                                        file:mr-4 file:py-2 file:px-4
                                        file:rounded-lg file:border-0
                                        file:text-sm file:font-semibold
                                        file:bg-indigo-50 file:text-indigo-700
                                        hover:file:bg-indigo-100
                                        dark:file:bg-indigo-900/30 dark:file:text-indigo-400
                                        cursor-pointer"
                                />
                                {completeFile && (
                                    <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                        Archivo seleccionado: {completeFile.name}
                                    </p>
                                )}
                            </div>

                            <Button
                                onClick={handleImportComplete}
                                disabled={!completeFile || isImporting}
                                className="w-full"
                            >
                                {isImporting ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Importando...
                                    </>
                                ) : (
                                    <>
                                        <Upload size={16} />
                                        Importar Casos
                                    </>
                                )}
                            </Button>
                        </div>
                    </div>
                </div>

                {/* RESULTADO DE IMPORTACIÓN DE CASOS */}
                {importResult && (
                    <div className="mt-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
                        <h4 className="font-semibold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
                            <CheckCircle className="text-green-500" size={20} />
                            Resultado de Importación
                        </h4>
                        
                        <div className="space-y-2 text-sm">
                            {importResult.casos_importados !== undefined && (
                                <p className="text-slate-700 dark:text-slate-300">
                                    ✅ Casos creados: <strong>{importResult.casos_importados}</strong>
                                </p>
                            )}
                            {importResult.casos_actualizados !== undefined && (
                                <p className="text-slate-700 dark:text-slate-300">
                                    🔄 Casos actualizados: <strong>{importResult.casos_actualizados}</strong>
                                </p>
                            )}
                            {importResult.observaciones_importadas !== undefined && importResult.observaciones_importadas > 0 && (
                                <p className="text-slate-700 dark:text-slate-300">
                                    📝 Observaciones importadas: <strong>{importResult.observaciones_importadas}</strong>
                                </p>
                            )}
                        </div>

                        {importResult.errores && importResult.errores.length > 0 && (
                            <div className="mt-4">
                                <h5 className="font-semibold text-red-600 dark:text-red-400 mb-2 flex items-center gap-2">
                                    <XCircle size={16} />
                                    Errores encontrados ({importResult.errores.length})
                                </h5>
                                <div className="max-h-40 overflow-y-auto space-y-1">
                                    {importResult.errores.slice(0, 10).map((error, idx) => (
                                        <p key={idx} className="text-xs text-red-600 dark:text-red-400">
                                            • {error}
                                        </p>
                                    ))}
                                    {importResult.errores.length > 10 && (
                                        <p className="text-xs text-slate-500 dark:text-slate-400 italic">
                                            ... y {importResult.errores.length - 10} errores más
                                        </p>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </Card>

            {/* SECCIÓN: USUARIOS */}
            <Card className="p-6">
                <div className="flex items-center gap-3 mb-6">
                    <Users className="text-emerald-500" size={24} />
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                        Usuarios
                    </h2>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* EXPORTAR USUARIOS */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2">
                            <Download size={20} />
                            Exportar Usuarios
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                            Exporta todos los usuarios del sistema (solo administradores).
                        </p>
                        <div className="flex gap-2">
                            <Button
                                variant="outline"
                                onClick={() => handleExportUsers('xlsx')}
                                disabled={isExportingUsers}
                                className="flex-1"
                            >
                                {isExportingUsers ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Exportando...
                                    </>
                                ) : (
                                    <>
                                        <Download size={16} />
                                        Exportar Excel
                                    </>
                                )}
                            </Button>
                            <Button
                                variant="outline"
                                onClick={() => handleExportUsers('csv')}
                                disabled={isExportingUsers}
                                className="flex-1"
                            >
                                {isExportingUsers ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Exportando...
                                    </>
                                ) : (
                                    <>
                                        <Download size={16} />
                                        Exportar CSV
                                    </>
                                )}
                            </Button>
                        </div>
                    </div>

                    {/* IMPORTAR USUARIOS */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2">
                            <Upload size={20} />
                            Importar Usuarios
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                            Importa usuarios desde Excel o CSV. Columnas: nombre, email, rol (opcional: password, is_active).
                        </p>

                        <div className="space-y-3">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Archivo de Usuarios
                                </label>
                                <input
                                    id="users-file"
                                    type="file"
                                    accept=".xlsx,.xls,.csv"
                                    onChange={handleUsersFileChange}
                                    className="block w-full text-sm text-slate-500 dark:text-slate-400
                                        file:mr-4 file:py-2 file:px-4
                                        file:rounded-lg file:border-0
                                        file:text-sm file:font-semibold
                                        file:bg-emerald-50 file:text-emerald-700
                                        hover:file:bg-emerald-100
                                        dark:file:bg-emerald-900/30 dark:file:text-emerald-400
                                        cursor-pointer"
                                />
                                {usersFile && (
                                    <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                        Archivo seleccionado: {usersFile.name}
                                    </p>
                                )}
                            </div>

                            <Button
                                onClick={handleImportUsers}
                                disabled={!usersFile || isImportingUsers}
                                className="w-full bg-emerald-600 hover:bg-emerald-700"
                            >
                                {isImportingUsers ? (
                                    <>
                                        <Loader2 className="animate-spin" size={16} />
                                        Importando...
                                    </>
                                ) : (
                                    <>
                                        <Upload size={16} />
                                        Importar Usuarios
                                    </>
                                )}
                            </Button>
                        </div>
                    </div>
                </div>

                {/* RESULTADO DE IMPORTACIÓN DE USUARIOS */}
                {userImportResult && (
                    <div className="mt-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
                        <h4 className="font-semibold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
                            <CheckCircle className="text-green-500" size={20} />
                            Resultado de Importación de Usuarios
                        </h4>
                        
                        <div className="space-y-2 text-sm">
                            {userImportResult.usuarios_importados !== undefined && (
                                <p className="text-slate-700 dark:text-slate-300">
                                    ✅ Usuarios creados: <strong>{userImportResult.usuarios_importados}</strong>
                                </p>
                            )}
                            {userImportResult.usuarios_actualizados !== undefined && (
                                <p className="text-slate-700 dark:text-slate-300">
                                    🔄 Usuarios actualizados: <strong>{userImportResult.usuarios_actualizados}</strong>
                                </p>
                            )}
                        </div>

                        {userImportResult.contraseñas_generadas && userImportResult.contraseñas_generadas.length > 0 && (
                            <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-300 dark:border-yellow-700 rounded">
                                <h5 className="font-semibold text-yellow-800 dark:text-yellow-300 mb-2 flex items-center gap-2">
                                    <AlertCircle size={16} />
                                    {userImportResult.advertencia}
                                </h5>
                                <div className="max-h-60 overflow-y-auto space-y-2">
                                    {userImportResult.contraseñas_generadas.map((user, idx) => (
                                        <div key={idx} className="text-xs bg-white dark:bg-slate-800 p-2 rounded border border-yellow-200 dark:border-yellow-800">
                                            <p className="font-semibold text-slate-900 dark:text-white">{user.nombre} ({user.email})</p>
                                            <p className="font-mono text-slate-700 dark:text-slate-300">Contraseña: <strong>{user.password}</strong></p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {userImportResult.errores && userImportResult.errores.length > 0 && (
                            <div className="mt-4">
                                <h5 className="font-semibold text-red-600 dark:text-red-400 mb-2 flex items-center gap-2">
                                    <XCircle size={16} />
                                    Errores encontrados ({userImportResult.errores.length})
                                </h5>
                                <div className="max-h-40 overflow-y-auto space-y-1">
                                    {userImportResult.errores.slice(0, 10).map((error, idx) => (
                                        <p key={idx} className="text-xs text-red-600 dark:text-red-400">
                                            • {error}
                                        </p>
                                    ))}
                                    {userImportResult.errores.length > 10 && (
                                        <p className="text-xs text-slate-500 dark:text-slate-400 italic">
                                            ... y {userImportResult.errores.length - 10} errores más
                                        </p>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </Card>

            {/* INFORMACIÓN Y AYUDA */}
            <Card className="p-6 bg-blue-50 dark:bg-blue-900/10 border-blue-200 dark:border-blue-800">
                <div className="flex items-start gap-3">
                    <AlertCircle className="text-blue-500 mt-1" size={20} />
                    <div className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
                        <h3 className="font-semibold text-slate-900 dark:text-white">Información Importante</h3>
                        <ul className="list-disc list-inside space-y-1 ml-2">
                            <li>El archivo Excel de casos debe contener hojas llamadas "Casos" y opcionalmente "Observaciones"</li>
                            <li>Las columnas requeridas para casos son: codigo, servicio_o_plataforma, estado, prioridad, motivo</li>
                            <li>Las columnas requeridas para usuarios son: nombre, email, rol</li>
                            <li>Si no se proporciona contraseña para usuarios nuevos, se generará una automáticamente</li>
                            <li>Los casos y usuarios existentes se actualizarán si se encuentran duplicados</li>
                        </ul>
                    </div>
                </div>
            </Card>
        </div>
    );
}
