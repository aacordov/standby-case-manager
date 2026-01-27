# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.3.0] - 2026-01-26

### 🎉 Resumen
Versión mayor con nuevas funcionalidades críticas: eliminación de casos, edición de observaciones, bulk updates mejorado, sistema de auditoría completo y testing comprehensivo.

### ✨ Added (Nuevas Funcionalidades)

#### Backend - Endpoints
- **DELETE /cases/{case_id}**: Endpoint para eliminar casos (solo ADMIN)
  - Validación estricta de permisos
  - CASCADE delete automático de observaciones, attachments y auditorías
  - Respuesta estructurada con confirmación
  
- **PATCH /cases/observations/{observation_id}**: Editar observaciones individuales
  - Control granular de permisos (usuario puede editar su propia observación)
  - ADMIN/INGRESO pueden editar cualquier observación
  - Campo `edited_at` actualizado automáticamente
  - Validación de propiedad de observación

- **POST /cases/bulk-update**: Operaciones masivas mejoradas
  - Acciones soportadas: CLOSE, ASSIGN, PRIORITY
  - Generación automática de auditoría por cada caso actualizado
  - Validación de permisos (INGRESO/ADMIN solamente)
  - Respuesta con contador de casos actualizados

- **GET /cases/{case_id}/timeline**: Timeline completo del caso
  - Eventos ordenados cronológicamente
  - Tipos: CREATE, OBSERVATION, AUDIT
  - Información de usuario por cada evento
  - Incluye detalles de cambios en auditorías

#### Backend - Modelos
- **Sistema de Auditoría**: Modelo `CaseAudit` implementado
  - Tipos de auditoría: CREATE, UPDATE, BULK_UPDATE, COMMENT, EVIDENCE, DELETE
  - Campo `details` JSON con old/new values
  - Relaciones con User y Case
  - Timestamp automático

- **Observaciones Refactorizadas**: Migración a entidades separadas
  - Modelo `Observation` independiente del caso
  - Campo `content` para el texto de la observación
  - Campos `created_at` y `edited_at` para tracking
  - Relación many-to-one con Case
  - Relación many-to-one con User (created_by)

- **Relaciones CASCADE**: Configuración correcta de integridad referencial
  - `Case -> Observation`: ondelete="CASCADE", passive_deletes=True
  - `Case -> Attachment`: ondelete="CASCADE", passive_deletes=True
  - `Case -> CaseAudit`: ondelete="CASCADE", passive_deletes=True
  - Prevención de datos huérfanos en la base de datos

#### Backend - Mejoras en Paginación
- **Respuesta estructurada** en GET /cases:
  ```json
  {
    "items": [...],      # Lista de casos
    "total": 100,        # Total de casos que cumplen filtros
    "skip": 0,           # Offset actual
    "limit": 20,         # Límite de resultados
    "page": 1,           # Página actual (1-indexed)
    "total_pages": 5     # Total de páginas disponibles
  }
  ```

#### Testing
- **21 Pruebas Nuevas** implementadas:
  - **6 pruebas de eliminación**: DELETE endpoint completo
    - `test_delete_case_as_admin_success`
    - `test_delete_case_as_ingreso_forbidden`
    - `test_delete_case_as_consulta_forbidden`
    - `test_delete_nonexistent_case`
    - `test_delete_case_cascade_observations`
    - `test_delete_case_cascade_audits`
  
  - **7 pruebas de observaciones**: PATCH endpoint completo
    - `test_update_own_observation_success`
    - `test_update_others_observation_as_admin`
    - `test_update_others_observation_as_ingreso`
    - `test_update_others_observation_forbidden`
    - `test_update_nonexistent_observation`
    - `test_update_observation_without_auth`
    - Tests adicionales de estructura
  
  - **4 pruebas de bulk updates**: POST bulk-update mejorado
    - `test_bulk_update_with_audit_creation`
    - `test_bulk_update_invalid_action`
    - `test_bulk_update_nonexistent_cases`
    - `test_bulk_update_audit_details`
  
  - **4 pruebas de timeline y auditoría**: GET timeline completo
    - `test_timeline_with_all_event_types`
    - `test_timeline_chronological_order`
    - `test_audit_details_structure`
    - `test_audit_appears_in_timeline`

- **Cobertura de Tests**:
  - Backend: 85% → 92% (+7%)
  - Módulo `cases.py`: 95% (+20%)
  - Módulo `models.py`: 88% (+8%)

#### Documentación
- **README actualizado** con todas las nuevas funcionalidades
- **API Reference completa** (docs/API_Reference.md) - Nuevo archivo
- **Testing Strategy** actualizada (backend/test/TESTING_STRATEGY.md)
- **Deployment Guide** con estrategias Docker productivo (docs/Deployment.md)
- **Troubleshooting Guide** expandida (docs/Troubleshooting.md) - Nuevo archivo
- **Análisis de Cobertura** (analisis_cobertura_pruebas.md) - Nuevo archivo
- **Guía de Despliegue Productivo** (estrategia_despliegue_produccion.md) - Nuevo archivo

### 🔄 Changed (Cambios)

#### Backend
- **Sistema de Observaciones**: Refactorización completa
  - Observaciones ahora son entidades separadas en lugar de un campo de texto
  - Campo legacy `observaciones` en Case ahora es opcional y deprecado
  - Al crear caso con observación inicial, se crea registro en tabla Observation
  - Al actualizar caso con nueva observación, se agrega a observaciones_list

- **Gestión de Permisos**: Control más granular
  - Eliminación de casos restringida exclusivamente a ADMIN
  - Edición de observaciones: usuario puede editar las suyas, ADMIN/INGRESO todas
  - Bulk updates requiere permisos de INGRESO o ADMIN

- **Respuestas API**: Estructuradas y consistentes
  - Paginación con metadata completa
  - Mensajes de error más descriptivos
  - Respuestas de eliminación con detalles del elemento eliminado

#### Modelos de Datos
- **Case Model**:
  - Agregadas relaciones con `observaciones_list`, `attachments`, `audit_logs`
  - Campo `observaciones` deprecado pero mantenido para compatibilidad
  - Configuración CASCADE en todas las relaciones

- **Observation Model**:
  - Nuevo modelo independiente
  - Campos: `id`, `case_id`, `content`, `created_at`, `edited_at`, `created_by_id`
  - Relaciones: `case` (many-to-one), `created_by` (many-to-one)

- **CaseAudit Model**:
  - Nuevo modelo para auditoría
  - Campos: `id`, `case_id`, `user_id`, `action`, `details`, `timestamp`
  - Relación con User para información del autor

### 🐛 Fixed (Correcciones)

#### Backend
- **Integridad Referencial**: Corrección de eliminaciones CASCADE
  - Agregado `ondelete="CASCADE"` en todas las foreign keys
  - Agregado `passive_deletes=True` en relaciones SQLModel
  - Prevención de datos huérfanos al eliminar casos

- **Permisos de Observaciones**: Control de acceso corregido
  - Usuario CONSULTA solo puede editar sus propias observaciones
  - Verificación correcta de propiedad antes de permitir edición
  - Mensajes de error claros cuando se deniega acceso

- **Tracking de Cambios**: Auditoría correcta
  - Generación automática de auditoría en updates
  - Detalles completos de cambios (old/new values)
  - Manejo correcto de enums en comparaciones

- **Eliminación de Casos**: Cleanup completo
  - CASCADE de todas las relaciones (observaciones, attachments, audits)
  - Validación de permisos antes de eliminar
  - Respuesta con confirmación de eliminación

#### Testing
- **Fixtures**: Corrección de dependencias circulares
  - Reorganización de fixtures en conftest.py
  - Uso correcto de `db_session` en fixtures
  - Limpieza de base de datos entre tests

- **Tests Asíncronos**: Manejo correcto de asyncio
  - Todos los tests de integración con `@pytest.mark.asyncio`
  - Uso correcto de `await` en operaciones de base de datos
  - Configuración de `asyncio_mode = auto` en pytest.ini

### 🔒 Security (Seguridad)

- **Control de Eliminación**: Solo ADMIN puede eliminar casos
- **Auditoría Completa**: Registro de todas las operaciones críticas
- **Validación de Permisos**: Verificación en cada endpoint sensible
- **Protección de Datos**: CASCADE configurado correctamente para prevenir datos huérfanos

### 📊 Performance

- **Queries Optimizadas**: Uso de `selectinload` para relaciones
  - `CaseReadWithDetails` carga observaciones y attachments de una vez
  - Timeline carga usuario con cada observación y auditoría
  - Reducción de N+1 queries

- **Paginación**: Queries count optimizadas
  - Query count separado para metadata
  - Aplicación correcta de filtros en ambos queries
  - Índices en campos de búsqueda frecuente

### ⚠️ Breaking Changes (Cambios Incompatibles)

Ninguno. Esta versión mantiene compatibilidad con 2.2.x

### 🗑️ Deprecated (Deprecado)

- **Case.observaciones** (campo de texto): Use `observaciones_list` (relación) en su lugar
  - El campo legacy se mantiene por compatibilidad pero se establece en `None` por defecto
  - Los nuevos casos deben usar el sistema de observaciones separadas

### 🔧 Infrastructure

- **Docker**: Configuraciones separadas para dev y prod
  - `docker-compose.yml`: Desarrollo con hot-reload
  - `docker-compose.prod.yml`: Producción con imágenes optimizadas
  - `Dockerfile.prod`: Multi-stage build para backend

- **Testing**: Scripts y configuración mejorados
  - `run_tests.sh`: Script unificado para ejecutar tests
  - Configuración de coverage más estricta (90% mínimo)
  - Markers adicionales en pytest para organización

---

## [2.2.3] - 2026-01-20

### 🔧 Fixed
- Corrección de import/export con observaciones múltiples
- Mejora en validación de archivos Excel
- Fix en timezone handling para búsquedas

### ✨ Added
- Soporte para importación legacy de bitácora antigua
- Exportación con todas las observaciones por caso

---

## [2.2.0] - 2026-01-15

### ✨ Added
- **Import/Export Module**: Módulo completo de importación/exportación
  - Soporte para Excel (XLSX), CSV, TSV
  - Importación con múltiples observaciones por caso
  - Validación de formato y datos

- **Dashboard de Estadísticas**: Visualizaciones mejoradas
  - Gráficos de distribución por estado
  - Gráficos de distribución por prioridad
  - Evolución temporal de casos

- **Filtros Avanzados**: Mejoras en búsqueda
  - Filtro por rango de fechas con presets (1M, 3M, 6M)
  - Filtro por servicio/plataforma
  - Filtro por responsable SBY
  - Búsqueda de texto en código y motivo

### 🔄 Changed
- UI/UX mejorada en formularios
- Componentes reutilizables optimizados
- Rendimiento de queries optimizado

---

## [2.1.0] - 2026-01-10

### ✨ Added
- **Command Palette**: Navegación rápida con Ctrl+K
- **Smart Avatars**: Avatares generados por hash de email
- **File Management**: Sistema de gestión de archivos adjuntos
  - Upload con drag & drop
  - Preview de imágenes y PDFs
  - Validación de tipos de archivo
  - Límite de tamaño configurable

### 🔄 Changed
- Sistema de notificaciones mejorado
- Transiciones y animaciones más fluidas
- Carga lazy de componentes pesados

---

## [2.0.0] - 2025-12-15

### 🎉 Major Release
Gran refactor de la aplicación con migración a tecnologías modernas.

### ✨ Added
- **Frontend Completo**: Migración de PHP a React
  - SPA con React 18 + Vite
  - TypeScript para type safety
  - TailwindCSS para estilos
  - React Query para estado del servidor
  - React Router para navegación

- **Backend Modernizado**: Actualización a FastAPI
  - API RESTful completa
  - Documentación automática (Swagger/ReDoc)
  - Validación con Pydantic
  - Autenticación JWT
  - ORM con SQLModel

- **Testing Infrastructure**: Suite completa de tests
  - Tests unitarios (backend y frontend)
  - Tests de integración
  - Coverage >85%

### 🔄 Changed
- Migración de MySQL a PostgreSQL
- Sistema de autenticación refactorizado
- Estructura de base de datos optimizada

### 🗑️ Removed
- Legacy PHP codebase
- jQuery dependencies
- Bootstrap (migrado a TailwindCSS)

---

## [1.2.0] - 2025-11-01

### ✨ Added
- Sistema de roles y permisos
- Gestión de usuarios
- Logs de auditoría básicos

### 🐛 Fixed
- Correcciones de seguridad en autenticación
- Fix de validación de formularios

---

## [1.1.0] - 2025-10-15

### ✨ Added
- Búsqueda de casos por múltiples criterios
- Paginación en listado de casos
- Exportación a Excel

### 🔄 Changed
- Mejoras en UI del dashboard
- Optimización de queries SQL

---

## [1.0.0] - 2025-10-01

### 🎉 Initial Release
Primera versión estable del sistema.

### Features
- CRUD completo de casos
- Sistema de autenticación básico
- Dashboard con estadísticas
- Gestión de estados de casos
- Prioridades configurables

---

## Formato de Versiones

El versionado sigue Semantic Versioning:
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Funcionalidad nueva compatible con versiones anteriores
- **PATCH**: Correcciones de bugs compatibles con versiones anteriores

## Categorías de Cambios

- **✨ Added**: Nuevas funcionalidades
- **🔄 Changed**: Cambios en funcionalidad existente
- **🗑️ Deprecated**: Funcionalidades obsoletas pero aún presentes
- **🗑️ Removed**: Funcionalidades eliminadas
- **🐛 Fixed**: Correcciones de bugs
- **🔒 Security**: Correcciones de seguridad
- **📊 Performance**: Mejoras de rendimiento
- **🔧 Infrastructure**: Cambios en infraestructura/DevOps
- **⚠️ Breaking Changes**: Cambios incompatibles con versiones anteriores

---

**Última actualización**: 2026-01-26
**Versión actual**: 2.3.0
