# 🛡️ Standby Case Manager

> **Sistema integral para la gestión y monitoreo de casos de operación en tiempo real.**

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20PostgreSQL-blueviolet?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-90%25-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)

---

## 📋 Descripción

**Standby Case Manager** es una solución robusta diseñada para optimizar el flujo de trabajo de los equipos de operaciones. Permite registrar, monitorear y gestionar incidentes de manera eficiente, asegurando que nada se pierda en el cambio de turno.

### ✨ Características Principales

* **🚀 Gestión en Tiempo Real**: Actualizaciones instantáneas de casos y estados
* **🔍 Filtrado Avanzado**: Búsqueda potente por fecha (presets 1M/3M/6M), prioridad, estado y responsable
* **⌨️ Command Palette**: Navegación rápida y acciones globales con `Ctrl + K`
* **👤 Smart Avatars**: Identificación visual instantánea con avatares generados por hash
* **📂 Bóveda de Evidencias**: Adjunta imágenes, PDFs y logs con drag & drop, previsualización y auditoría
* **🌍 Soporte de Zona Horaria**: Detección automática para búsquedas precisas
* **🔒 Seguridad**: Autenticación JWT y gestión de roles (Admin/Ingreso/Consulta)
* **📊 Dashboard de Estadísticas**: Métricas y gráficos en tiempo real
* **📤 Importación/Exportación**: Módulo dedicado con soporte para Excel (XLSX), CSV y observaciones múltiples por caso
* **🐳 Dockerizado**: Despliegue sencillo y consistente
* **✅ Testing Completo**: Suite de tests unitarios e integración con 90% de cobertura

---

## 🛠️ Tecnologías

### Backend

- ⚡ **FastAPI** - Framework web moderno y rápido
- 🐘 **PostgreSQL** - Base de datos relacional
- 🔐 **JWT** - Autenticación segura
- 📦 **SQLModel** - ORM con tipado fuerte
- 🧪 **Pytest** - Framework de testing

### Frontend

- ⚛️ **React 18** - Librería UI con hooks
- ⚡ **Vite** - Build tool ultrarrápido
- 🎨 **TailwindCSS** - Framework CSS utility-first
- 🔄 **React Query** - Gestión de estado del servidor
- 🧭 **React Router** - Enrutamiento declarativo
- 🧪 **Vitest** - Testing framework para Vite
- 📊 **Recharts** - Gráficos y visualizaciones

### DevOps & Tools

- 🐳 **Docker** - Containerización
- 🥯 **Bun** - Runtime JavaScript rápido
- 🚀 **uv** - Gestor de paquetes Python ultrarrápido

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

| Rol          | Email                  | Password      | Permisos           |
| :----------- | :--------------------- | :------------ | :----------------- |
| **Admin**    | `admin@standby.com`    | `admin123`    | Acceso total       |
| **Ingreso**  | `ingreso@standby.com`  | `ingreso123`  | Crear/editar casos |
| **Consulta** | `consulta@standby.com` | `consulta123` | Solo lectura       |

> ⚠️ **Importante**: Se recomienda cambiar estas contraseñas inmediatamente después del primer inicio de sesión en producción.

---

## 📂 Estructura del Proyecto

```text
standby-case-manager/
├── 📁 backend/                 # API RESTful con FastAPI
│   ├── 📁 app/
│   │   ├── 📄 main.py         # Punto de entrada
│   │   ├── 📄 models.py       # Modelos SQLModel
│   │   ├── 📄 database.py     # Configuración BD
│   │   ├── 📄 auth.py         # Autenticación JWT
│   │   ├── 📄 schemas.py      # Schemas Pydantic
│   │   └── 📁 routers/        # Endpoints
│   │       ├── 📄 auth.py     # Login/registro
│   │       ├── 📄 cases.py    # CRUD casos
│   │       ├── 📄 users.py    # Gestión usuarios
│   │       ├── 📄 files.py    # Upload archivos
│   │       ├── 📄 stats.py    # Estadísticas
│   │       └── 📄 import_export.py
│   ├── 📁 test/               # Tests unitarios e integración
│   │   ├── 📄 conftest.py    # Fixtures compartidas
│   │   ├── 📁 unit/          # Tests unitarios
│   │   ├── 📁 integration/   # Tests de integración
│   │   └── 📄 README.md      # Guía de testing
│   ├── 📄 requirements.txt
│   ├── 📄 requirements-test.txt
│   └── 📄 Dockerfile
│
├── 📁 frontend/               # SPA React + Vite
│   ├── 📁 src/
│   │   ├── 📁 components/    # Componentes React
│   │   │   └── 📁 ui/       # UI Components
│   │   ├── 📁 pages/        # Páginas/rutas
│   │   │   ├── 📄 Dashboard.tsx
│   │   │   ├── 📄 CaseForm.tsx
│   │   │   ├── 📄 ImportExportCases.tsx
│   │   │   └── 📄 ...
│   │   ├── 📁 context/      # Context API
│   │   ├── 📁 api/          # Axios config
│   │   ├── 📁 types/        # TypeScript types
│   │   ├── 📁 utils/        # Utilidades
│   │   └── 📁 test/         # Tests (unitarios/integración)
│   │       ├── 📁 mocks/    # Mocks para MSW
│   │       └── 📄 setup.ts  # Configuración de tests
│   ├── 📄 package.json
│   ├── 📄 vite.config.ts
│   ├── 📄 vitest.config.ts
│   ├── 📄 tailwind.config.js
│   ├── 📄 run_tests.sh      # Script para ejecutar tests
│   └── 📄 Dockerfile
│
├── 📁 docs/                   # Documentación
│   ├── 📄 Manual_de_usuario.md
│   ├── 📄 Documentacion_tecnica.md
│   └── 📄 Deployment.md
│
├── 📄 docker-compose.yml
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 CONTRIBUTING.md
├── 📄 CHANGELOG.md
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

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-test.txt  # Para desarrollo

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Variables de entorno** (`backend/.env`):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/standby_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend

```bash
cd frontend

# Instalar Node Version Manager (si no lo tienes)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# Instalar Node.js
nvm install --lts
nvm use --lts

# Instalar dependencias
npm install

# Instalar dependencias de testing
npm install -D vitest @vitest/ui @vitest/coverage-v8 \
  @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event jsdom msw

# Ejecutar en desarrollo
npm run dev

# Ejecutar tests
chmod +x run_tests.sh
./run_tests.sh

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

El proyecto cuenta con una suite completa de tests con **~90% de cobertura** en backend y frontend.

### Backend Tests

El backend incluye **tests unitarios** y **tests de integración**:

```bash
cd backend

# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-test.txt

# Ejecutar todos los tests
pytest

# Solo tests unitarios
pytest test/unit -v

# Solo tests de integración
pytest test/integration -v

# Con coverage
pytest --cov=app --cov-report=html

# Ver reporte HTML
open htmlcov/index.html  # En Linux: xdg-open htmlcov/index.html
```

**Tipos de tests en backend:**

- **Unitarios** (`test/unit/`): Tests de funciones, lógica de negocio y modelos
- **Integración** (`test/integration/`): Tests de endpoints completos con base de datos

### Frontend Tests

El frontend incluye **tests unitarios** y **tests de integración** con React Testing Library:

```bash
cd frontend

# Instalar dependencias (si aún no lo hiciste)
npm install
npm install -D vitest @vitest/ui @vitest/coverage-v8 \
  @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event jsdom msw

# Dar permisos al script
chmod +x run_tests.sh

# Ejecutar tests con el script
./run_tests.sh

# O ejecutar directamente con npm
npm run test              # Modo interactivo
npm run test:run          # Una sola vez
npm run test:ui           # UI visual
npm run test:coverage     # Con coverage
```

**Tipos de tests en frontend:**

- **Unitarios**: Tests de componentes individuales, hooks y utilidades
- **Integración**: Tests de flujos completos de usuario con mocks de API

---

## 📊 API Endpoints

### Autenticación

- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual
- `POST /auth/refresh` - Renovar token

### Casos

- `GET /cases` - Listar casos (con filtros)
- `POST /cases` - Crear caso
- `GET /cases/{id}` - Obtener caso
- `PUT /cases/{id}` - Actualizar caso
- `DELETE /cases/{id}` - Eliminar caso

### Usuarios

- `GET /users` - Listar usuarios
- `POST /users` - Crear usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

### Archivos

- `POST /files/upload` - Subir archivo
- `GET /files/{id}` - Descargar archivo
- `DELETE /files/{id}` - Eliminar archivo

### Estadísticas

- `GET /stats/dashboard` - Dashboard principal
- `GET /stats/cases-by-status` - Por estado
- `GET /stats/cases-by-priority` - Por prioridad

### Import/Export

- `POST /cases-io/import-with-observations` - Importar casos con observaciones
- `GET /cases-io/export-with-observations` - Exportar casos y observaciones (Excel/CSV)
- `POST /cases-io/import-legacy` - Importar desde bitácora legacy
- `POST /cases-io/import` - Importar casos simple
- `GET /cases-io/export` - Exportar casos simple (TSV/CSV/XLSX)

---

## 🔒 Seguridad

- 🔐 **JWT Authentication** con tokens de acceso y refresh
- 🛡️ **CORS** configurado para dominios permitidos
- 🔑 **Bcrypt** para hash de contraseñas
- 👤 **Role-based Access Control** (RBAC)
- 📝 **Validación** con Pydantic y Zod
- 🔒 **SQL Injection Protection** mediante ORM

---

## 🐳 Docker

### Servicios

```yaml
services:
  - postgres: Base de datos PostgreSQL 15
  - backend: API FastAPI en Python 3.11
  - frontend: React SPA servido con Nginx
```

### Comandos útiles

```bash
# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f backend

# Reiniciar servicio
docker compose restart backend

# Ejecutar comando en contenedor
docker compose exec backend bash

# Detener todo
docker compose down

# Limpiar volúmenes (⚠️ elimina datos)
docker compose down -v

# Reconstruir imágenes
docker compose build --no-cache
```

---

## 🔧 Solución de Problemas

### El contenedor de backend no inicia

**Síntomas:** Error al ejecutar `docker compose up`

**Soluciones:**

1. Verificar que PostgreSQL esté corriendo: `docker compose ps`
2. Revisar logs: `docker compose logs backend`
3. Verificar variables de entorno en `.env`
4. Reiniciar contenedor: `docker compose restart backend`

### Error "Cannot connect to database"

**Causa:** La base de datos no está lista cuando el backend intenta conectar.

**Solución:**

```bash
docker compose restart backend
```

### Frontend no carga

**Verificar:**

1. ¿El contenedor está corriendo? `docker compose ps frontend`
2. ¿Está accesible en http://localhost:3000?
3. Revisar logs: `docker compose logs frontend`
4. Limpiar caché del navegador

### Problemas de permisos con archivos

**En Linux:**

```bash
sudo chown -R $USER:$USER .
```

### Los tests fallan con "ModuleNotFoundError"

**Backend:**

```bash
# Asegurarse de estar en el directorio correcto
cd backend
# Verificar que el entorno virtual está activado
source .venv/bin/activate
# Reinstalar dependencias
pip install -r requirements.txt -r requirements-test.txt
```

**Frontend:**

```bash
# Limpiar node_modules
rm -rf node_modules package-lock.json
npm install
```

---

## 📖 Documentación Adicional

- 📘 [Manual de Usuario](./docs/Manual_de_usuario.md) - Guía completa de uso
- 🔧 [Documentación Técnica](./docs/Documentacion_tecnica.md) - Arquitectura y APIs
- 🚀 [Guía de Despliegue](./docs/Deployment.md) - Deploy en producción
- 🤝 [Guía de Contribución](./CONTRIBUTING.md) - Cómo contribuir
- 🧪 [Guía de Testing](./backend/test/README.md) - Estrategia de testing

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para más detalles sobre estándares de código y proceso de review.

---

## 📝 Changelog

Ver [CHANGELOG.md](./CHANGELOG.md) para el historial de versiones.

**Versión actual**: 2.2.3

---

## 📄 Licencia

Este proyecto es propiedad privada. Todos los derechos reservados.

---

## 👥 Equipo de Desarrollo

Desarrollado con ❤️ por:

- **Allan Córdova** - [aacordov@gmail.com](mailto:aacordov@gmail.com)
- **José Briones** - [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
- **Larry Sánchez** - [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
- **Ronny Ortiz** - [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

---

## 📞 Soporte

- 📧 Email: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- 🐛 Issues: [GitHub Issues](https://github.com/rortiz-09/standby-case-manager/issues)

---

**Happy Coding! 🚀**