# 🛡️ Standby Case Manager

> **Sistema integral para la gestión y monitoreo de casos de operación en tiempo real.**

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL-blueviolet?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-92%25-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)

---

## 📋 Descripción

**Standby Case Manager** es una solución robusta diseñada para optimizar el flujo de trabajo de los equipos de operaciones. Permite registrar, monitorear y gestionar incidentes de manera eficiente, asegurando que nada se pierda en el cambio de turno.

### ✨ Características Principales

#### 🎯 Gestión de Casos
* **🚀 Gestión en Tiempo Real**: Actualizaciones instantáneas de casos y estados
* **🔍 Filtrado Avanzado**: Búsqueda potente por fecha (presets 1M/3M/6M), prioridad, estado y responsable
* **📊 Paginación Inteligente**: Sistema de paginación optimizado con metadata (total, página, total de páginas)
* **⌨️ Command Palette**: Navegación rápida y acciones globales con `Ctrl + K`
* **🗑️ Eliminación Controlada**: Solo administradores pueden eliminar casos (con CASCADE a relaciones)

#### 📝 Sistema de Observaciones
* **📋 Observaciones como Entidades**: Sistema refactorizado con observaciones separadas del caso principal
* **✏️ Edición Granular**: Edita observaciones individuales con control de permisos
* **👤 Trazabilidad**: Cada observación mantiene registro de quién la creó y cuándo
* **🕒 Historial de Edición**: Campo `edited_at` para tracking de modificaciones

#### 🔍 Auditoría y Timeline
* **📜 Timeline Completo**: Visualización cronológica de toda la actividad del caso
* **🔎 Sistema de Auditoría**: Registro automático de cambios con detalles (old/new values)
* **📊 Tipos de Eventos**:
  - `CREATE`: Creación del caso
  - `UPDATE`: Actualizaciones individuales
  - `BULK_UPDATE`: Actualizaciones masivas
  - `COMMENT`: Nuevas observaciones
  - `EVIDENCE`: Adjuntos de evidencias
  - `DELETE`: Eliminaciones

#### ⚡ Operaciones Masivas
* **📦 Bulk Update**: Actualización masiva de múltiples casos simultáneamente
  - Cerrar múltiples casos
  - Asignar responsable masivamente
  - Cambiar prioridad en lote
* **📈 Auditoría de Bulk**: Cada operación masiva genera registros de auditoría individuales

#### 📂 Gestión de Evidencias
* **🗂️ Bóveda de Evidencias**: Adjunta imágenes, PDFs y logs con drag & drop
* **👁️ Previsualización**: Visualización directa de archivos adjuntos
* **🔗 Relaciones CASCADE**: Eliminación automática de adjuntos al eliminar caso
* **📊 Metadata**: Tracking completo de tamaño, tipo y fecha de archivos

#### 🔒 Seguridad y Roles
* **🔐 Autenticación JWT**: Tokens seguros con refresh automático
* **👥 Control de Acceso Basado en Roles (RBAC)**:
  - **ADMIN**: Acceso total, incluyendo eliminación de casos
  - **INGRESO**: Crear y editar casos, bulk updates
  - **CONSULTA**: Solo lectura, puede editar sus propias observaciones
* **🛡️ Permisos Granulares**: Control fino sobre operaciones de observaciones

#### 📊 Análisis y Reportes
* **📈 Dashboard de Estadísticas**: Métricas y gráficos en tiempo real
* **📤 Importación/Exportación**: Módulo dedicado con soporte para Excel (XLSX), CSV
  - Importación con múltiples observaciones por caso
  - Exportación con timeline completo
  - Compatibilidad con formato legacy
* **🌍 Soporte de Zona Horaria**: Detección automática para búsquedas precisas
* **👤 Smart Avatars**: Identificación visual instantánea con avatares generados por hash

#### 🛠️ Desarrollo y Testing
* **🐳 Dockerizado**: Despliegue sencillo y consistente
* **✅ Testing Completo**: Suite de tests unitarios e integración con 92% de cobertura
* **🔄 CI/CD Ready**: Preparado para pipelines de integración continua
* **📝 Documentación Completa**: Guías técnicas y manuales de usuario

---

## 🚀 Guía de Inicio Rápido

La forma más sencilla de ejecutar el proyecto es utilizando **Docker**. Olvídate de instalar dependencias manualmente.

### Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo

### 1️⃣ Instalación

Clona el repositorio y navega al directorio:

```bash
git clone git@github.com:rortiz-09/standby-case-manager.git
cd standby-case-manager
```

### 2️⃣ Configuración Inicial

Crea el archivo de variables de entorno:

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus valores (opcional para desarrollo)
# Los valores por defecto funcionan para ambiente local
```

### 3️⃣ Ejecución

Levanta todo el entorno con un solo comando:

```bash
docker compose up --build
```

> ☕ **Primera vez**: Puede tardar unos minutos descargando imágenes y construyendo contenedores

### 4️⃣ Acceso

| Servicio      | URL                                                        | Descripción               |
| :------------ | :--------------------------------------------------------- | :------------------------ |
| **Frontend**  | [http://localhost:3000](http://localhost:3000)             | Interfaz principal        |
| **API Docs**  | [http://localhost:8000/docs](http://localhost:8000/docs)   | Swagger UI                |
| **API ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Documentación alternativa |

---

## 🔐 Credenciales por Defecto

| Rol          | Email                  | Password      | Permisos                              |
| :----------- | :--------------------- | :------------ | :------------------------------------ |
| **Admin**    | `admin@example.com`    | `admin123`    | Acceso total + eliminación de casos  |
| **Ingreso**  | `ingreso@example.com`  | `ingreso123`  | Crear/editar casos + bulk updates     |
| **Consulta** | `consulta@example.com` | `consulta123` | Lectura + editar propias observaciones|

> ⚠️ **Importante**: Se recomienda cambiar estas contraseñas inmediatamente después del primer inicio de sesión en producción.

---

## 📂 Estructura del Proyecto

```text
standby-case-manager/
├── 📁 backend/                 # API RESTful con FastAPI
│   ├── 📁 app/
│   │   ├── 📄 main.py         # Punto de entrada
│   │   ├── 📄 models.py       # Modelos SQLModel con CASCADE
│   │   ├── 📄 database.py     # Configuración BD
│   │   ├── 📄 auth.py         # Autenticación JWT
│   │   ├── 📄 schemas.py      # Schemas Pydantic adicionales
│   │   └── 📁 routers/        # Endpoints
│   │       ├── 📄 auth.py     # Login/registro
│   │       ├── 📄 cases.py    # CRUD casos + bulk + timeline
│   │       ├── 📄 users.py    # Gestión usuarios
│   │       ├── 📄 files.py    # Upload/download archivos
│   │       ├── 📄 stats.py    # Estadísticas y dashboard
│   │       └── 📄 import_export.py # Import/Export Excel/CSV
│   ├── 📁 test/               # Tests unitarios e integración
│   │   ├── 📄 conftest.py    # Fixtures compartidas
│   │   ├── 📁 unit/          # Tests unitarios
│   │   │   ├── 📄 test_auth_unit.py
│   │   │   └── 📄 test_models.py
│   │   ├── 📁 integration/   # Tests de integración
│   │   │   ├── 📄 test_auth_integration.py
│   │   │   ├── 📄 test_cases_integration.py  # 40+ tests
│   │   │   └── 📄 test_users_integration.py
│   │   ├── 📄 README.md      # Guía completa de testing
│   │   └── 📄 TESTING_STRATEGY.md
│   ├── 📄 requirements.txt
│   ├── 📄 requirements-test.txt
│   ├── 📄 Dockerfile          # Para desarrollo
│   └── 📄 Dockerfile.prod     # Para producción (recomendado)
│
├── 📁 frontend/               # SPA React + Vite
│   ├── 📁 src/
│   │   ├── 📁 components/    # Componentes React
│   │   │   ├── 📁 ui/       # UI Components (Headless UI)
│   │   │   ├── 📄 CaseTimeline.tsx      # Timeline visual
│   │   │   ├── 📄 ObservationEditor.tsx # Editor de obs
│   │   │   └── 📄 BulkActions.tsx       # Acciones masivas
│   │   ├── 📁 pages/        # Páginas/rutas
│   │   │   ├── 📄 Dashboard.tsx
│   │   │   ├── 📄 CaseForm.tsx
│   │   │   ├── 📄 CaseDetail.tsx        # Con timeline
│   │   │   ├── 📄 ImportExportCases.tsx
│   │   │   └── 📄 ...
│   │   ├── 📁 context/      # Context API
│   │   ├── 📁 api/          # Axios config + endpoints
│   │   ├── 📁 types/        # TypeScript types
│   │   ├── 📁 utils/        # Utilidades
│   │   └── 📁 test/         # Tests (unitarios/integración)
│   ├── 📄 package.json
│   ├── 📄 vite.config.ts
│   ├── 📄 vitest.config.ts
│   └── 📄 tailwind.config.js
│
├── 📁 docs/                   # Documentación
│   ├── 📄 Manual_de_usuario.md
│   ├── 📄 Documentacion_tecnica.md (actualizada)
│   ├── 📄 API_Reference.md (nueva)
│   ├── 📄 Testing_Guide.md (actualizada)
│   └── 📄 Deployment.md (con estrategias prod)
│
├── 📄 docker-compose.yml          # Desarrollo
├── 📄 docker-compose.prod.yml     # Producción (recomendado)
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 CONTRIBUTING.md
├── 📄 CHANGELOG.md (actualizado)
└── 📄 README.md
```

---

## 💻 Desarrollo Local (Manual)

Si deseas ejecutar los servicios fuera de Docker para desarrollo:

### Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Instalar dependencias con uv (más rápido)
pip install uv
uv pip install --system -r requirements.txt -r requirements-test.txt

# O con pip tradicional
pip install -r requirements.txt
pip install -r requirements-test.txt

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Variables de entorno** (`backend/.env`):

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/standby_db
REDIS_URL=redis://localhost:6379  # Opcional
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend

```bash
cd frontend

# Instalar Node.js (LTS recomendado)
# Con nvm:
nvm install --lts
nvm use --lts

# O instalar Bun (más rápido)
curl -fsSL https://bun.sh/install | bash

# Instalar dependencias
npm install
# O con bun:
bun install

# Ejecutar en desarrollo
npm run dev
# O con bun:
bun run dev

# Ejecutar tests
npm run test
# O con bun:
bun test

# Build para producción
npm run build
```

**Variables de entorno** (`frontend/.env`):

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Standby Case Manager
```

---

## 🧪 Testing

El proyecto cuenta con una suite completa de tests con **~92% de cobertura** en backend y **~88% en frontend**.

### Backend Tests

El backend incluye **tests unitarios** y **tests de integración**:

```bash
cd backend

# Activar entorno virtual
source .venv/bin/activate

# Ejecutar todos los tests
pytest

# Solo tests unitarios
pytest test/unit -v

# Solo tests de integración
pytest test/integration -v

# Tests específicos por funcionalidad
pytest -m cases      # Solo tests de casos
pytest -m auth       # Solo tests de autenticación
pytest -m users      # Solo tests de usuarios

# Con coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Ver reporte HTML
open htmlcov/index.html  # En Linux: xdg-open htmlcov/index.html

# Tests en paralelo (más rápido)
pytest -n auto
```

**Cobertura por módulo:**

| Módulo | Cobertura | Tests |
|--------|-----------|-------|
| `cases.py` (router) | 95% | 40+ |
| `auth.py` | 92% | 12 |
| `users.py` | 90% | 10 |
| `models.py` | 88% | 8 |
| `import_export.py` | 85% | 6 |

**Tests principales:**

- ✅ **Eliminación de casos** (6 pruebas)
  - DELETE por ADMIN
  - Permisos denegados INGRESO/CONSULTA
  - CASCADE de observaciones/attachments/audits
  - Casos inexistentes

- ✅ **Edición de observaciones** (7 pruebas)
  - Editar propia observación
  - Permisos por rol (ADMIN/INGRESO/CONSULTA)
  - Actualización de `edited_at`
  - Observaciones inexistentes

- ✅ **Bulk updates** (4 pruebas)
  - Cerrar múltiples casos
  - Asignar responsable masivamente
  - Cambiar prioridad en lote
  - Generación de auditorías

- ✅ **Timeline y auditoría** (4 pruebas)
  - Timeline completo
  - Eventos ordenados cronológicamente
  - Auditorías en UPDATE/BULK_UPDATE
  - Estructura de detalles

Ver [backend/test/README.md](./backend/test/README.md) para guía completa de testing.

### Frontend Tests

```bash
cd frontend

# Ejecutar tests
npm run test              # Modo interactivo
npm run test:run          # Una sola vez
npm run test:ui           # UI visual
npm run test:coverage     # Con coverage

# O con script
chmod +x run_tests.sh
./run_tests.sh
```

---

## 📊 API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión (retorna access + refresh token)
- `GET /auth/me` - Obtener usuario actual
- `POST /auth/refresh` - Renovar token
- `POST /auth/change-password` - Cambiar contraseña

### Casos

#### Básico
- `GET /cases` - Listar casos con filtros y paginación
  - Query params: `skip`, `limit`, `status`, `priority`, `service`, `sby_responsable`, `search`, `start_date`, `end_date`
  - Respuesta incluye metadata de paginación
- `POST /cases` - Crear caso (INGRESO/ADMIN)
  - Crea observación inicial si se proporciona
- `GET /cases/{id}` - Obtener caso con observaciones y attachments
- `PATCH /cases/{id}` - Actualizar caso (INGRESO/ADMIN)
  - Genera auditoría automáticamente
- `DELETE /cases/{id}` - **Eliminar caso (SOLO ADMIN)** 🆕
  - CASCADE delete de observaciones, attachments, audits

#### Avanzado 🆕
- `POST /cases/bulk-update` - Actualización masiva (INGRESO/ADMIN)
  - Body: `{"ids": [1,2,3], "action": "CLOSE|ASSIGN|PRIORITY", "value": "..."}`
  - Genera auditoría por cada caso
- `GET /cases/{id}/timeline` - Timeline completo del caso
  - Retorna eventos: CREATE, OBSERVATION, AUDIT
  - Ordenado cronológicamente
- `PATCH /cases/observations/{observation_id}` - Editar observación
  - Usuario puede editar su propia observación
  - ADMIN/INGRESO pueden editar cualquier observación
  - Actualiza campo `edited_at`

### Usuarios
- `GET /users` - Listar usuarios (ADMIN)
- `POST /users` - Crear usuario (ADMIN)
- `GET /users/{id}` - Obtener usuario
- `PATCH /users/{id}` - Actualizar usuario (ADMIN o propio)
- `DELETE /users/{id}` - Eliminar usuario (ADMIN)

### Archivos
- `POST /files/upload` - Subir archivo adjunto a caso
- `GET /files/download/{filename}` - Descargar archivo
- `DELETE /files/{id}` - Eliminar archivo (ADMIN/INGRESO)

### Estadísticas
- `GET /stats/dashboard` - Dashboard con métricas generales
- `GET /stats/cases-by-status` - Distribución por estado
- `GET /stats/cases-by-priority` - Distribución por prioridad
- `GET /stats/cases-over-time` - Evolución temporal

### Import/Export
- `POST /cases-io/import-with-observations` - Importar casos con múltiples observaciones
  - Formato: Excel/CSV con columnas específicas
- `GET /cases-io/export-with-observations` - Exportar casos completos
  - Formato: Excel/CSV con todas las observaciones
- `POST /cases-io/import-legacy` - Importar desde bitácora legacy
- `POST /cases-io/import` - Importación simple
- `GET /cases-io/export` - Exportación simple (TSV/CSV/XLSX)

Ver [docs/API_Reference.md](./docs/API_Reference.md) para documentación detallada de cada endpoint.

---

## 🔒 Seguridad

### Autenticación
- 🔐 **JWT Authentication** con access tokens (30 min) y refresh tokens (7 días)
- 🔄 **Token Refresh** automático antes de expiración
- 🔑 **Bcrypt** para hash de contraseñas (costo: 12)
- 🚫 **Revocación de tokens** mediante blacklist (opcional con Redis)

### Autorización
- 👤 **Role-based Access Control (RBAC)** con 3 niveles:
  - **ADMIN**: Control total
  - **INGRESO**: Crear/editar/bulk updates
  - **CONSULTA**: Lectura + editar propias observaciones
- 🔒 **Permisos Granulares** en endpoints sensibles
- ✅ **Validación de Permisos** en cada operación crítica

### Protección
- 🛡️ **CORS** configurado para dominios permitidos
- 📝 **Validación de entrada** con Pydantic en backend y Zod en frontend
- 🔒 **SQL Injection Protection** mediante ORM parameterizado
- 🔐 **XSS Protection** con sanitización de inputs
- 📋 **CSRF Protection** con tokens en forms (opcional)
- 🚨 **Rate Limiting** (opcional con Redis)

### Auditoría
- 📜 **Logging completo** de operaciones críticas
- 🔍 **Auditoría automática** de cambios en casos
- 👤 **Tracking de usuario** en cada operación
- 🕒 **Timestamps** automáticos (created_at, updated_at)

---

## 🐳 Docker

### Configuraciones Disponibles

#### Desarrollo (`docker-compose.yml`)
```yaml
services:
  db: PostgreSQL 15 con healthcheck
  redis: Redis Alpine (opcional)
  backend: FastAPI con hot-reload y volúmenes montados
  frontend: Vite dev server con hot-reload
```

Características:
- ✅ Hot-reload habilitado
- ✅ Volúmenes montados para edición en vivo
- ✅ Logs detallados
- ✅ Debug mode

#### Producción (`docker-compose.prod.yml`) 🆕
```yaml
services:
  db: PostgreSQL 15 con backups automáticos
  redis: Redis con persistencia
  backend: Imagen optimizada sin volúmenes de código
  frontend: Build estático servido por Nginx
```

Características:
- ✅ Código incluido en imagen (inmutable)
- ✅ Multi-stage builds (imágenes más pequeñas)
- ✅ Usuario no-root por seguridad
- ✅ Health checks configurados
- ✅ Restart policies
- ✅ Resource limits

### Comandos Útiles

```bash
# === DESARROLLO ===

# Levantar servicios
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f

# Ver logs de servicio específico
docker compose logs -f backend

# Reiniciar servicio
docker compose restart backend

# Ejecutar comando en contenedor
docker compose exec backend bash
docker compose exec backend pytest

# Detener todo
docker compose down

# Limpiar volúmenes (⚠️ elimina datos)
docker compose down -v

# === PRODUCCIÓN ===

# Build de imagen productiva
docker build -f backend/Dockerfile.prod -t standby-backend:1.0.0 ./backend

# Levantar en producción
docker compose -f docker-compose.prod.yml up -d

# Ver estado de servicios
docker compose -f docker-compose.prod.yml ps

# Ver logs de producción
docker compose -f docker-compose.prod.yml logs -f

# Actualizar imagen
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d

# === MANTENIMIENTO ===

# Reconstruir imágenes sin cache
docker compose build --no-cache

# Limpiar imágenes antiguas
docker system prune -a

# Ver uso de recursos
docker stats

# Backup de base de datos
docker compose exec db pg_dump -U user standby_db > backup.sql

# Restaurar base de datos
docker compose exec -T db psql -U user standby_db < backup.sql
```

### Estrategia de Despliegue Recomendada

Para producción, **SIEMPRE** usa imágenes con código incluido:

```bash
# 1. Build de imagen versionada
docker build -f backend/Dockerfile.prod \
  -t standby-backend:2.3.0 \
  ./backend

# 2. Tag adicionales
docker tag standby-backend:2.3.0 standby-backend:latest
docker tag standby-backend:2.3.0 standby-backend:prod

# 3. Push a registry
docker push yourregistry/standby-backend:2.3.0

# 4. Deploy en servidor
docker pull yourregistry/standby-backend:2.3.0
docker compose -f docker-compose.prod.yml up -d
```

Ver [docs/Deployment.md](./docs/Deployment.md) para guía completa de despliegue.

---

## 🔧 Solución de Problemas

### El contenedor de backend no inicia

**Síntomas:** Error `Cannot connect to database` o backend crashea

**Soluciones:**

1. Verificar que PostgreSQL esté listo:
```bash
docker compose ps
docker compose logs db
```

2. Verificar health check:
```bash
docker compose exec db pg_isready -U user -d standby_db
```

3. Revisar variables de entorno:
```bash
docker compose config
```

4. Reiniciar con dependencias:
```bash
docker compose down
docker compose up -d
```

### Tests fallan con "ModuleNotFoundError"

**Backend:**
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt -r test/requirements-dev.txt
python -m pytest
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run test
```

### Error "Database is locked" en tests

**Causa:** SQLite usado en tests simultáneos

**Solución:**
```bash
# Ejecutar tests serialmente
pytest -n 0

# O limpiar archivos de test
rm -f test.db .coverage
```

### Problemas de permisos con archivos adjuntos

**En Linux:**
```bash
# Dar permisos al directorio uploads
sudo chown -R $USER:$USER backend/uploads
chmod 755 backend/uploads
```

**En Docker:**
```bash
# Recrear volumen
docker compose down -v
docker compose up -d
```

### Frontend no conecta con backend

**Verificar:**

1. Backend está corriendo:
```bash
curl http://localhost:8000/docs
```

2. CORS configurado correctamente en backend:
```python
# app/main.py
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
]
```

3. Variable de entorno en frontend:
```bash
# frontend/.env
VITE_API_URL=http://localhost:8000
```

### Migrations de base de datos

**Crear migration:**
```bash
# Todavía no implementado, usar scripts SQL directos
docker compose exec db psql -U user -d standby_db
```

**Aplicar cambios de esquema:**
```bash
# Recrear todo (⚠️ elimina datos)
docker compose down -v
docker compose up -d
```

---

## 📖 Documentación Adicional

### Documentación Técnica
- 📘 [Manual de Usuario](./docs/Manual_de_usuario.md) - Guía completa de uso
- 🔧 [Documentación Técnica](./docs/Documentacion_tecnica.md) - Arquitectura y decisiones técnicas
- 📊 [API Reference](./docs/API_Reference.md) - 🆕 Documentación completa de todos los endpoints
- 🧪 [Testing Guide](./backend/test/README.md) - Guía exhaustiva de testing

### Guías de Desarrollo
- 🚀 [Deployment Guide](./docs/Deployment.md) - Deploy en producción con Docker
- 🤝 [Contributing Guide](./CONTRIBUTING.md) - Cómo contribuir al proyecto
- 📝 [Changelog](./CHANGELOG.md) - 🆕 Historial de versiones detallado

### Recursos Internos
- 🔍 [Testing Strategy](./backend/test/TESTING_STRATEGY.md) - Estrategia y patrones de testing
- 🐛 [Troubleshooting](./docs/Troubleshooting.md) - Soluciones a problemas comunes
- 🔒 [Security Guidelines](./docs/Security.md) - Mejores prácticas de seguridad

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor sigue este proceso:

1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Escribe tests** para tu código nuevo
4. **Asegura que los tests pasen**: `pytest && npm run test`
5. **Verifica cobertura**: `pytest --cov=app --cov-fail-under=90`
6. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
7. **Push** a la rama (`git push origin feature/AmazingFeature`)
8. **Abre un Pull Request**

### Estándares de Código

#### Backend (Python)
```bash
# Format code
black app/ test/

# Sort imports
isort app/ test/

# Lint
flake8 app/ test/ --max-line-length=100

# Type check
mypy app/
```

#### Frontend (TypeScript)
```bash
# Format code
npm run format

# Lint
npm run lint

# Type check
npm run type-check
```

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para más detalles.

---

## 📝 Changelog

### [2.3.0] - 2026-01-26 🆕

#### Added
- **Backend**:
  - ✨ Endpoint DELETE /cases/{case_id} (solo ADMIN)
  - ✨ Endpoint PATCH /observations/{observation_id}
  - ✨ Endpoint POST /cases/bulk-update para operaciones masivas
  - ✨ Endpoint GET /cases/{case_id}/timeline
  - ✨ Sistema de auditoría con modelo CaseAudit
  - ✨ Observaciones como entidades separadas
  - ✨ Paginación mejorada con metadata completa
  - ✨ Relaciones CASCADE configuradas correctamente
  
- **Testing**:
  - ✅ 21 pruebas nuevas para funcionalidades críticas
  - ✅ Tests de eliminación con CASCADE (6 pruebas)
  - ✅ Tests de edición de observaciones (7 pruebas)
  - ✅ Tests de bulk updates (4 pruebas)
  - ✅ Tests de auditoría y timeline (4 pruebas)
  - ✅ Cobertura aumentada a 92%

- **Documentación**:
  - 📚 API Reference completa
  - 📚 Guía de despliegue con Docker productivo
  - 📚 Estrategia de testing actualizada
  - 📚 Troubleshooting guide expandida

#### Changed
- 🔄 Sistema de observaciones refactorizado
- 🔄 Modelos con relaciones CASCADE mejoradas
- 🔄 Respuestas de paginación estructuradas
- 🔄 Permisos granulares en observaciones

#### Fixed
- 🐛 Integridad referencial en eliminaciones
- 🐛 Permisos de edición de observaciones
- 🐛 Tracking de cambios en auditoría
- 🐛 Limpieza CASCADE de relaciones

### [2.2.3] - Anterior
- Ver [CHANGELOG.md](./CHANGELOG.md) completo

---

## 📄 Licencia

Este proyecto es propiedad privada. Todos los derechos reservados.

**© 2024-2026 Standby Case Manager Team**

---

## 👥 Equipo de Desarrollo

Desarrollado con ❤️ por:

| Nombre | Email | GitHub |
|--------|-------|--------|
| **Allan Córdova** | [aacordov@gmail.com](mailto:aacordov@gmail.com) | [@aacordova](https://github.com/aacordov) |
| **José Briones** | [josmbrio@gmail.com](mailto:josmbrio@gmail.com) | [@josmbrio](https://github.com/josmbrio) |
| **Larry Sánchez** | [lajasanc@gmail.com](mailto:lajasanc@gmail.com) | [@lajasanchez](https://github.com/lajasanc) |
| **Ronny Ortiz** | [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com) | [@rortiz-09](https://github.com/rortiz-09) |

---

## 📞 Soporte

### Canales de Soporte

- 📧 **Email**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/rortiz-09/standby-case-manager/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rortiz-09/standby-case-manager/discussions)

### Horario de Soporte

- **Lunes a Viernes**: 9:00 AM - 6:00 PM (GMT-5)
- **Respuesta esperada**: 24-48 horas

---

## 🌟 Agradecimientos

Agradecimientos especiales a:

- **FastAPI** por el framework excepcional
- **React** por la librería UI potente
- **PostgreSQL** por la base de datos confiable
- **Docker** por simplificar el deployment
- **La comunidad open-source** por todas las herramientas increíbles

---

**Happy Coding! 🚀**

*"La excelencia es un viaje, no un destino"*
