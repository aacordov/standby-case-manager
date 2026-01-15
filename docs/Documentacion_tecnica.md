# 🔧 Documentación Técnica - Standby Case Manager

## Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Backend - FastAPI](#backend---fastapi)
3. [Frontend - React](#frontend---react)
4. [Base de Datos](#base-de-datos)
5. [Autenticación y Seguridad](#autenticación-y-seguridad)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Deployment](#deployment)

---

## 🏗️ Arquitectura del Sistema

### Visión General

Standby Case Manager sigue una arquitectura de tres capas:

```
┌─────────────────────────────────────────────┐
│           FRONTEND (React + Vite)           │
│   ┌─────────────────────────────────────┐   │
│   │  UI Components (Tailwind)           │   │
│   │  State Management (React Query)     │   │
│   │  Routing (React Router)             │   │
│   └─────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST (Axios)
                   │
┌──────────────────▼──────────────────────────┐
│           BACKEND (FastAPI)                 │
│   ┌─────────────────────────────────────┐   │
│   │  API Routers                        │   │
│   │  Business Logic                     │   │
│   │  Authentication (JWT)               │   │
│   │  File Upload/Processing             │   │
│   └─────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │ SQLModel ORM
                   │
┌──────────────────▼──────────────────────────┐
│           DATABASE (PostgreSQL)             │
│   ┌─────────────────────────────────────┐   │
│   │  Tables: users, cases, files        │   │
│   │  Indexes & Constraints              │   │
│   │  Migrations                         │   │
│   └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Stack Tecnológico

#### Backend
- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.14
- **Database Driver**: asyncpg + psycopg2-binary
- **Auth**: python-jose, bcrypt, passlib
- **Validation**: Pydantic 2.0
- **File Handling**: aiofiles
- **Data Processing**: pandas, openpyxl, xlsxwriter
- **Cache**: Redis (opcional)

#### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Language**: TypeScript 5.2
- **Styling**: TailwindCSS 3.3
- **HTTP Client**: Axios 1.6
- **State Management**: React Query 5.90
- **Forms**: React Hook Form 7.48
- **Routing**: React Router DOM 6.18
- **UI Components**: Headless UI 2.2
- **Charts**: Recharts 2.10
- **Icons**: Lucide React 0.290
- **Animations**: Framer Motion 12.23

#### Database
- **Primary**: PostgreSQL 15+
- **Development**: SQLite (opcional)

#### DevOps
- **Containerization**: Docker & Docker Compose
- **Process Manager**: uvicorn (backend), Vite dev server (frontend)

---

## 🔙 Backend - FastAPI

### Estructura de Directorios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada
│   ├── database.py          # Configuración de DB
│   ├── models.py            # Modelos SQLModel
│   ├── schemas.py           # Schemas Pydantic
│   ├── auth.py              # Utilidades de autenticación
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Endpoints de autenticación
│       ├── cases.py         # CRUD de casos
│       ├── users.py         # Gestión de usuarios
│       ├── files.py         # Upload/download de archivos
│       ├── stats.py         # Estadísticas y métricas
│       └── import_export.py # Import/Export Excel/PDF
├── test/
│   ├── fixtures/
│   ├── unit/
│   └── integration/
├── uploads/                  # Archivos subidos
├── requirements.txt
├── .env
└── Dockerfile
```

### Modelos de Datos (SQLModel)

#### User

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: str = Field(default="consulta")  # admin, ingreso, consulta
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Case

```python
class Case(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    priority: str = Field(default="media")  # alta, media, baja
    status: str = Field(default="abierto")  # abierto, en_progreso, resuelto, cerrado
    case_type: str  # incidente, problema, solicitud
    responsible_id: int = Field(foreign_key="user.id")
    deadline: datetime | None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: int = Field(foreign_key="user.id")
```

#### File

```python
class File(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    case_id: int = Field(foreign_key="case.id")
    uploaded_by: int = Field(foreign_key="user.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
```

### Configuración de Base de Datos

```python
# database.py
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/standby")

# Engine síncrono
engine = create_engine(DATABASE_URL)

# Engine asíncrono (opcional)
async_engine = create_async_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

### Autenticación JWT

```python
# auth.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### Endpoints Principales

#### Auth Router (`routers/auth.py`)

```python
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm):
    """
    Autenticación de usuario
    Returns: access_token, token_type
    """
    
@router.get("/me")
async def get_current_user(current_user: User = Depends(get_current_user)):
    """
    Obtiene información del usuario autenticado
    """
```

#### Cases Router (`routers/cases.py`)

```python
@router.get("/")
async def list_cases(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    priority: str | None = None,
    responsible_id: int | None = None
):
    """
    Lista casos con filtros opcionales
    """

@router.post("/")
async def create_case(case: CaseCreate):
    """
    Crea un nuevo caso
    Required role: admin, ingreso
    """

@router.get("/{case_id}")
async def get_case(case_id: int):
    """
    Obtiene un caso específico
    """

@router.put("/{case_id}")
async def update_case(case_id: int, case: CaseUpdate):
    """
    Actualiza un caso
    Required role: admin, ingreso
    """

@router.delete("/{case_id}")
async def delete_case(case_id: int):
    """
    Elimina un caso
    Required role: admin
    """
```

#### Files Router (`routers/files.py`)

```python
@router.post("/upload")
async def upload_file(
    file: UploadFile,
    case_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Sube un archivo y lo asocia a un caso
    Max size: 10MB
    """

@router.get("/{file_id}")
async def download_file(file_id: int):
    """
    Descarga un archivo
    Returns: FileResponse
    """

@router.delete("/{file_id}")
async def delete_file(file_id: int):
    """
    Elimina un archivo
    Required role: admin, ingreso
    """
```

### Middleware y CORS

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚛️ Frontend - React

### Estructura de Directorios

```
frontend/
├── src/
│   ├── main.tsx             # Entry point
│   ├── App.tsx              # Root component
│   ├── api/
│   │   └── axios.ts         # Axios instance
│   ├── components/
│   │   ├── ui/              # UI components reutilizables
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── ...
│   │   ├── CaseCard.tsx
│   │   ├── CaseForm.tsx
│   │   ├── CaseList.tsx
│   │   ├── FileUpload.tsx
│   │   ├── Navbar.tsx
│   │   └── ...
│   ├── context/
│   │   ├── ThemeContext.tsx
│   │   └── ToastContext.tsx
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Cases.tsx
│   │   ├── CaseDetail.tsx
│   │   ├── Users.tsx
│   │   └── NotFound.tsx
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   ├── utils/
│   │   ├── cn.ts            # Tailwind merge utility
│   │   ├── auth.ts          # Auth helpers
│   │   └── date.ts          # Date utilities
│   └── test/
│       ├── test-utils.tsx   # Testing utilities
│       └── mocks/           # MSW mocks
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── vitest.config.ts
```

### Configuración de Axios

```typescript
// api/axios.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Request interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### React Query Setup

```typescript
// main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### Custom Hooks

```typescript
// hooks/useCases.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/axios';

export function useCases(filters?: CaseFilters) {
  return useQuery({
    queryKey: ['cases', filters],
    queryFn: async () => {
      const { data } = await api.get('/cases', { params: filters });
      return data;
    },
  });
}

export function useCreateCase() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (newCase: CaseCreate) => {
      const { data } = await api.post('/cases', newCase);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
    },
  });
}
```

### Componentes Clave

#### Protected Route

```typescript
// components/ProtectedRoute.tsx
export function ProtectedRoute({ children, requiredRole }: Props) {
  const user = useUser();
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/unauthorized" />;
  }
  
  return <>{children}</>;
}
```

#### Theme Provider

```typescript
// context/ThemeContext.tsx
export function ThemeProvider({ children }: Props) {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved as 'light' | 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches 
      ? 'dark' 
      : 'light';
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Routing

```typescript
// App.tsx
const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: <ProtectedRoute><Layout /></ProtectedRoute>,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'cases', element: <Cases /> },
      { path: 'cases/:id', element: <CaseDetail /> },
      { path: 'users', element: <ProtectedRoute requiredRole="admin"><Users /></ProtectedRoute> },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
]);
```

---

## 🗄️ Base de Datos

### Schema PostgreSQL

```sql
-- Users table
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'consulta',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cases table
CREATE TABLE case (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(50) DEFAULT 'media',
    status VARCHAR(50) DEFAULT 'abierto',
    case_type VARCHAR(50),
    responsible_id INTEGER REFERENCES user(id),
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES user(id)
);

-- Files table
CREATE TABLE file (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    case_id INTEGER REFERENCES case(id) ON DELETE CASCADE,
    uploaded_by INTEGER REFERENCES user(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_case_status ON case(status);
CREATE INDEX idx_case_priority ON case(priority);
CREATE INDEX idx_case_responsible ON case(responsible_id);
CREATE INDEX idx_case_created_at ON case(created_at);
CREATE INDEX idx_file_case ON file(case_id);
```

### Migraciones

Las migraciones se manejan manualmente con scripts SQL o usando herramientas como Alembic.

```bash
# Instalar Alembic
pip install alembic

# Inicializar Alembic
alembic init migrations

# Crear migración
alembic revision --autogenerate -m "Initial schema"

# Aplicar migraciones
alembic upgrade head
```

---

## 🔒 Autenticación y Seguridad

### Flujo de Autenticación

```
1. Usuario envía credenciales (email, password)
   ↓
2. Backend valida credenciales
   ↓
3. Backend genera JWT token
   ↓
4. Frontend almacena token en localStorage
   ↓
5. Frontend incluye token en cada request (Authorization header)
   ↓
6. Backend valida token en cada endpoint protegido
```

### JWT Token Structure

```json
{
  "sub": "user@example.com",
  "role": "admin",
  "exp": 1706548800
}
```

### Roles y Permisos

| Endpoint | Admin | Ingreso | Consulta |
|:---------|:------|:--------|:---------|
| GET /cases | ✅ | ✅ | ✅ |
| POST /cases | ✅ | ✅ | ❌ |
| PUT /cases | ✅ | ✅ | ❌ |
| DELETE /cases | ✅ | ❌ | ❌ |
| GET /users | ✅ | ❌ | ❌ |
| POST /users | ✅ | ❌ | ❌ |

### Seguridad Adicional

- **CORS**: Configurado para dominios específicos
- **Rate Limiting**: 100 requests/minuto por IP
- **SQL Injection**: Prevenido por ORM (SQLModel)
- **XSS**: Sanitización de inputs en frontend
- **CSRF**: Tokens en formularios sensibles
- **Password Policy**: Mínimo 8 caracteres, 1 mayúscula, 1 número

---

## 📡 API Reference

### Authentication

#### POST /auth/login

**Request:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /auth/me

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "admin",
  "is_active": true
}
```

### Cases

#### GET /cases

**Query Parameters:**
- `skip`: int (default: 0)
- `limit`: int (default: 100)
- `status`: string (abierto, en_progreso, resuelto, cerrado)
- `priority`: string (alta, media, baja)
- `responsible_id`: int

**Response:**
```json
[
  {
    "id": 1,
    "title": "Incidente crítico",
    "description": "Descripción detallada",
    "priority": "alta",
    "status": "abierto",
    "case_type": "incidente",
    "responsible_id": 2,
    "deadline": "2026-01-25T10:00:00Z",
    "created_at": "2026-01-19T08:00:00Z",
    "updated_at": "2026-01-19T08:00:00Z",
    "created_by": 1
  }
]
```

#### POST /cases

**Request:**
```json
{
  "title": "Nuevo caso",
  "description": "Descripción",
  "priority": "media",
  "case_type": "solicitud",
  "responsible_id": 2,
  "deadline": "2026-01-25T10:00:00Z"
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Nuevo caso",
  ...
}
```

### Files

#### POST /files/upload

**Request (multipart/form-data):**
```
file: <binary>
case_id: 1
```

**Response:**
```json
{
  "id": 1,
  "filename": "abc123.pdf",
  "original_filename": "documento.pdf",
  "file_size": 1024000,
  "mime_type": "application/pdf",
  "case_id": 1,
  "uploaded_at": "2026-01-19T08:00:00Z"
}
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Solo tests unitarios
pytest test/unit/

# Solo tests de integración
pytest test/integration/
```

### Frontend Tests

```bash
cd frontend

# Ejecutar tests
bun run test

# Modo watch
bun run test:watch

# UI visual
bun run test:ui

# Coverage
bun run test:coverage
```

### Estructura de Tests

```typescript
// __tests__/Login.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Login from '../Login';

describe('Login Page', () => {
  it('should render login form', () => {
    render(<Login />);
    expect(screen.getByText('Iniciar Sesión')).toBeInTheDocument();
  });

  it('should successfully login', async () => {
    const user = userEvent.setup();
    render(<Login />);
    
    await user.type(screen.getByRole('textbox'), 'admin@example.com');
    await user.type(screen.getByLabelText(/contraseña/i), 'admin123');
    await user.click(screen.getByRole('button', { name: /entrar/i }));
    
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });
});
```

---

## 🚀 Deployment

### Variables de Entorno

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/standby_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
```

**Frontend (.env)**
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Standby Case Manager
```

### Docker Deployment

```bash
# Build y ejecutar
docker compose up --build -d

# Ver logs
docker compose logs -f

# Escalar servicios
docker compose up -d --scale backend=3
```

### Producción

Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para instrucciones detalladas.

---

**Última actualización**: Enero 2026
**Versión**: 2.2.3