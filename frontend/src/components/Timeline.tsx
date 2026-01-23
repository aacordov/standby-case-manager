import { motion } from 'framer-motion';
import { ArrowRight, AlertTriangle, User, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { clsx } from 'clsx';
import { Avatar } from './ui/Avatar';

interface TimelineItem {
    type: 'OBSERVATION' | 'AUDIT' | 'CREATE';
    id: number;
    content?: string; // For observation and CREATE
    action?: string; // For audit and CREATE
    details?: Record<string, any>; // For audit and CREATE
    created_at: string;
    user_name?: string;
    user_id?: number;
}

interface TimelineProps {
    items: TimelineItem[];
    currentUserId?: number;
}

export function Timeline({ items, currentUserId }: TimelineProps) {
    if (items.length === 0) {
        return <div className="text-center text-slate-400 py-8 italic">No hay historial disponible.</div>;
    }

    return (
        <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent dark:before:via-slate-700">
            {items.map((item, index) => {
                const isMe = item.type === 'OBSERVATION' && item.user_id === currentUserId;
                const isCreate = item.type === 'CREATE';

                return (
                    <motion.div
                        key={`${item.type}-${item.id}`}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className={clsx(
                            "relative flex items-center justify-between md:justify-normal group",
                            isMe ? "flex-row-reverse md:flex-row-reverse" : "flex-row"
                        )}
                    >
                        {/* Icon / Dot */}
                        <div className={clsx(
                            "flex items-center justify-center w-10 h-10 rounded-full shadow shrink-0 z-10 bg-white dark:bg-slate-800",
                            "md:absolute md:left-1/2 md:-translate-x-1/2", // Center line position
                            item.type === 'OBSERVATION' ? "p-0 border-0" : "border border-white dark:border-gray-900"
                        )}>
                            {item.type === 'OBSERVATION' ? (
                                <Avatar name={item.user_name || 'Desconocido'} size="md" />
                            ) : isCreate ? (
                                <User size={16} className="text-emerald-500" />
                            ) : item.action === 'UPDATE' ? (
                                <ArrowRight size={16} className="text-blue-500" />
                            ) : item.action === 'BULK_UPDATE' ? (
                                <AlertTriangle size={16} className="text-orange-500" />
                            ) : (item.action === 'EVIDENCE' || item.details?.filename) ? (
                                <FileText size={16} className="text-indigo-500" />
                            ) : (
                                <User size={16} className="text-emerald-500" />
                            )}
                        </div>

                        {/* Content Card */}
                        <div className={clsx(
                            "w-[calc(100%-4rem)] md:w-[calc(50%-2rem)] p-4 rounded-xl border shadow-sm transition-all hover:shadow-md",
                            // Margin to clear content from center line
                            isMe ? "mr-auto md:mr-auto md:ml-0" : "ml-auto md:ml-auto md:mr-0",

                            item.type === 'OBSERVATION'
                                ? (isMe
                                    ? "bg-indigo-50 dark:bg-indigo-900/20 border-indigo-100 dark:border-indigo-900/30 rounded-tr-none"
                                    : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-tl-none")
                                : isCreate
                                    ? "bg-emerald-50 dark:bg-emerald-900/20 border-emerald-100 dark:border-emerald-900/30"
                                    : "bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700 border-dashed"
                        )}>
                            {/* Header */}
                            <div className={clsx(
                                "flex items-center mb-2 gap-2",
                                isMe ? "justify-end flex-row-reverse" : "justify-between"
                            )}>
                                <span className={clsx(
                                    "text-xs font-bold",
                                    item.type === 'OBSERVATION' ? "text-slate-700 dark:text-slate-200" :
                                    isCreate ? "text-emerald-700 dark:text-emerald-300" :
                                    "text-slate-500 dark:text-slate-400"
                                )}>
                                    {item.user_name || (isMe ? 'Yo' : 'Usuario')}
                                </span>
                                <time className="text-[10px] text-slate-400 font-mono">
                                    {new Date(item.created_at).toLocaleString()}
                                </time>
                            </div>

                            {/* Body */}
                            {item.type === 'OBSERVATION' ? (
                                <div className={clsx(
                                    "text-sm text-slate-600 dark:text-slate-300 prose prose-sm dark:prose-invert max-w-none break-words",
                                    isMe ? "text-right" : "text-left"
                                )}>
                                    <ReactMarkdown components={{
                                        // @ts-ignore
                                        p: ({ node, ...props }) => <p className="mb-0 break-words whitespace-pre-wrap" {...props} />
                                    }}>
                                        {item.content || ''}
                                    </ReactMarkdown>
                                </div>
                            ) : isCreate ? (
                                <div className="text-xs space-y-2">
                                    <strong className="block text-emerald-700 dark:text-emerald-300 uppercase tracking-wider text-[10px] mb-2">CASO CREADO</strong>
                                    {item.content && (
                                        <div className="bg-white/50 dark:bg-black/20 rounded border border-emerald-200 dark:border-emerald-700/50 p-2">
                                            <p className="text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">Motivo:</p>
                                            <p className="text-xs text-slate-600 dark:text-slate-300 whitespace-pre-wrap">{item.content}</p>
                                        </div>
                                    )}
                                    {item.details && (
                                        <div className="bg-white/50 dark:bg-black/20 rounded border border-emerald-200 dark:border-emerald-700/50 p-2 space-y-1.5 text-[11px]">
                                            {item.details.servicio && (
                                                <div className="grid grid-cols-[auto_1fr] gap-x-2 items-baseline">
                                                    <span className="font-semibold text-slate-500 dark:text-slate-400">Servicio:</span>
                                                    <span className="text-slate-600 dark:text-slate-300">{item.details.servicio}</span>
                                                </div>
                                            )}
                                            {item.details.prioridad && (
                                                <div className="grid grid-cols-[auto_1fr] gap-x-2 items-baseline">
                                                    <span className="font-semibold text-slate-500 dark:text-slate-400">Prioridad:</span>
                                                    <span className="text-slate-600 dark:text-slate-300">{item.details.prioridad}</span>
                                                </div>
                                            )}
                                            {item.details.sby_responsable && (
                                                <div className="grid grid-cols-[auto_1fr] gap-x-2 items-baseline">
                                                    <span className="font-semibold text-slate-500 dark:text-slate-400">Responsable:</span>
                                                    <span className="text-slate-600 dark:text-slate-300">{item.details.sby_responsable}</span>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div className="text-xs space-y-2">
                                    <strong className="block text-slate-700 dark:text-slate-200 uppercase tracking-wider text-[10px]">{item.action}</strong>
                                    {(item.action === 'EVIDENCE' || item.details?.filename) ? (
                                        <div className="bg-white/50 dark:bg-black/20 rounded border border-slate-200 dark:border-slate-700/50 p-2 flex items-center gap-2">
                                            <div className="p-1 bg-indigo-100 dark:bg-indigo-900/30 rounded text-indigo-600 dark:text-indigo-400">
                                                <FileText size={14} />
                                            </div>
                                            <div className="text-[11px] font-mono text-slate-600 dark:text-slate-300">
                                                <span className="font-semibold block">{item.details?.filename || 'Archivo desconocido'}</span>
                                                <span className="text-slate-400">
                                                    {item.details?.size ? `${(item.details.size / 1024).toFixed(1)} KB` : ''}
                                                </span>
                                            </div>
                                        </div>
                                    ) : item.details && Object.keys(item.details).length > 0 && (
                                        <div className="bg-white/50 dark:bg-black/20 rounded border border-slate-200 dark:border-slate-700/50 p-2 space-y-1.5">
                                            {Object.entries(item.details).map(([key, diff]: [string, any]) => {
                                                // Si diff es un objeto con old y new, es un cambio
                                                if (diff && typeof diff === 'object' && ('old' in diff || 'new' in diff)) {
                                                    return (
                                                        <div key={key} className="grid grid-cols-[auto_1fr] gap-x-2 gap-y-1 items-baseline font-mono text-[11px]">
                                                            <span className="font-semibold text-slate-500 dark:text-slate-400 capitalize">{key.replace(/_/g, ' ')}:</span>
                                                            <div className="flex flex-wrap items-center gap-1.5">
                                                                {diff.old && (
                                                                    <>
                                                                        <span className="text-red-500 line-through bg-red-50 dark:bg-red-900/20 px-1.5 py-0.5 rounded decoration-2 break-all">{diff.old}</span>
                                                                        <ArrowRight size={10} className="text-slate-300 shrink-0" />
                                                                    </>
                                                                )}
                                                                <span className="text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20 px-1.5 py-0.5 rounded font-medium break-all">{diff.new ?? '?'}</span>
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            })}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </motion.div>
                );
            })}
        </div>
    );
}
