# 🔧 Documentación Técnica - Standby Case Manager v2.3.0

## Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Backend - FastAPI](#backend---fastapi)
3. [Frontend - React](#frontend---react)
4. [Base de Datos](#base-de-datos)
5. [Autenticación y Seguridad](#autenticación-y-seguridad)
6. [Nuevas Funcionalidades v2.3.0](#nuevas-funcionalidades-v230) 🆕
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [API Reference](#api-reference)

---

## 🏗️ Arquitectura del Sistema

### Visión General

Standby Case Manager sigue una arquitectura de tres capas con separación clara de responsabilidades:

```
┌─────────────────────────────────────────────┐
│       FRONTEND (React 18 + Vite)            │
│   ┌─────────────────────────────────────┐   │
│   │  UI Components (Tailwind + Headless)│   │
│   │  State Management (React Query)     │   │
│   │  Routing (React Router v6)          │   │
│   │  Forms (React Hook Form + Zod)      │   │
│   └─────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST + JWT
                   │ Axios Client
┌──────────────────▼──────────────────────────┐
│         BACKEND (FastAPI + Python)          │
│   ┌─────────────────────────────────────┐   │
│   │  API Routers (RESTful)              │   │
│   │  Business Logic Layer               │   │
│   │  Authentication (JWT + Bcrypt)      │   │
│   │  File Upload/Processing             │   │
│   │  Import/Export (Pandas)             │   │
│   │  Audit System 🆕                    │   │
│   └─────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │ SQLModel ORM (AsyncIO)
                   │ asyncpg + psycopg2
┌──────────────────▼──────────────────────────┐
│        DATABASE (PostgreSQL 15+)            │
│   ┌─────────────────────────────────────┐   │
│   │  Tables: users, cases, observations │   │
│   │  Audit: case_audit 🆕               │   │
│   │  Attachments: attachments           │   │
│   │  Indexes & Constraints              │   │
│   │  CASCADE Relations 🆕               │   │
│   └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

       ┌──────────────────────────┐
       │  CACHE (Redis) Optional  │
       │  - Session Storage       │
       │  - Query Cache           │
       └──────────────────────────┘
```

### Stack Tecnológico Completo

#### Backend
- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.14 (sobre SQLAlchemy 2.0)
- **Database Driver**: asyncpg (async) + psycopg2-binary (sync)
- **Auth**: python-jose[cryptography], passlib[bcrypt]
- **Validation**: Pydantic 2.5+
- **File Handling**: aiofiles, python-multipart
- **Data Processing**: pandas 2.1+, openpyxl, xlsxwriter
- **Cache**: redis, fastapi-cache2 (opcional)
- **Testing**: pytest 8.0, pytest-asyncio, httpx

#### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Language**: TypeScript 5.2
- **Styling**: TailwindCSS 3.3
- **HTTP Client**: Axios 1.6
- **State Management**: React Query (TanStack Query) 5.90
- **Forms**: React Hook Form 7.48 + Zod 3.22
- **Routing**: React Router DOM 6.18
- **UI Components**: Headless UI 2.2, Radix UI
- **Charts**: Recharts 2.10
- **Icons**: Lucide React 0.290
- **Animations**: Framer Motion 12.23
- **Testing**: Vitest, React Testing Library

#### Database
- **Primary**: PostgreSQL 15+ (con soporte para JSONB)
- **Development**: SQLite (para tests)
- **Migrations**: Alembic (próximamente)

#### DevOps
- **Containerization**: Docker 24+ & Docker Compose 2.23+
- **Process Manager**: uvicorn (ASGI server)
- **Web Server**: Nginx (para frontend en producción)
- **CI/CD**: GitHub Actions (configurado)

---

## 🔙 Backend - FastAPI

### Estructura de Directorios

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada ASGI
│   ├── database.py              # Config DB + Session Manager
│   ├── models.py                # Modelos SQLModel (ORM)
│   ├── schemas.py               # Schemas adicionales Pydantic
│   ├── auth.py                  # JWT + Password hashing
│   └── routers/                 # Endpoints organizados
│       ├── __init__.py
│       ├── auth.py              # Login, refresh, me
│       ├── cases.py             # CRUD casos + bulk + timeline 🆕
│       ├── users.py             # CRUD usuarios
│       ├── files.py             # Upload/download archivos
│       ├── stats.py             # Dashboard y métricas
│       └── import_export.py     # Import/Export Excel/CSV
├── test/                        # Suite de tests
│   ├── conftest.py              # Fixtures compartidas
│   ├── unit/                    # Tests unitarios
│   └── integration/             # Tests de integración
├── uploads/                     # Archivos adjuntos (dev)
├── requirements.txt             # Dependencias producción
├── requirements-test.txt        # Dependencias testing
├── Dockerfile                   # Imagen desarrollo
├── Dockerfile.prod 🆕          # Imagen producción optimizada
└── pytest.ini                   # Configuración pytest
```

### Modelos de Datos (app/models.py)

#### User Model
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    rol: UserRole = Field(default=UserRole.CONSULTA)
    is_active: bool = Field(default=True)
```

#### Case Model (Mejorado 🆕)
```python
class Case(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(unique=True, index=True)
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin: Optional[datetime] = None
    estado: CaseStatus = Field(default=CaseStatus.ABIERTO)
    sby_responsable: Optional[str] = None
    servicio_o_plataforma: str
    prioridad: Priority = Field(default=Priority.MEDIO)
    motivo: str = Field(default="")
    observaciones: Optional[str] = None  # Legacy - DEPRECATED
    creado_por_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 🆕 Relaciones con CASCADE
    observaciones_list: List["Observation"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"passive_deletes": True}
    )
    attachments: List["Attachment"] = Relationship(
        back_populates="case",
        sa_relationship_kwargs={"passive_deletes": True}
    )
    audit_logs: List["CaseAudit"] = Relationship(
        sa_relationship_kwargs={"passive_deletes": True}
    )
```

#### Observation Model 🆕
```python
class Observation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(foreign_key="case.id", ondelete="CASCADE")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    edited_at: Optional[datetime] = None
    created_by_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    case: Optional[Case] = Relationship(back_populates="observaciones_list")
    created_by: Optional[User] = Relationship()
```

#### CaseAudit Model 🆕
```python
class CaseAudit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(foreign_key="case.id", ondelete="CASCADE")
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    action: CaseAuditType  # CREATE, UPDATE, BULK_UPDATE, etc.
    details: Dict = Field(default={}, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship()
```

### Endpoints Principales

Ver [API_REFERENCE.md](./API_REFERENCE.md) para documentación completa.

#### Nuevos Endpoints v2.3.0 🆕

1. **DELETE /cases/{case_id}**
   - Solo ADMIN
   - CASCADE delete de observaciones, attachments, audits
   
2. **PATCH /cases/observations/{observation_id}**
   - Control de permisos granular por rol
   - Actualiza `edited_at` automáticamente

3. **POST /cases/bulk-update**
   - Acciones: CLOSE, ASSIGN, PRIORITY
   - Auditoría automática por cada caso

4. **GET /cases/{case_id}/timeline**
   - Timeline cronológico completo
   - Eventos: CREATE, OBSERVATION, AUDIT

### Autenticación JWT

```python
# Generación de token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificación de token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # ... obtener usuario de DB
```

### Sistema de Auditoría 🆕

La auditoría se registra automáticamente en operaciones críticas:

```python
# Ejemplo de auditoría en UPDATE
if audit_details:
    audit = CaseAudit(
        case_id=db_case.id,
        user_id=current_user.id,
        action=CaseAuditType.UPDATE,
        details=audit_details,  # {"campo": {"old": valor_antiguo, "new": valor_nuevo}}
        timestamp=datetime.utcnow()
    )
    session.add(audit)
```

---

## ⚛️ Frontend - React

### Estructura de Directorios

```
frontend/
├── src/
│   ├── main.tsx                   # Punto de entrada
│   ├── App.tsx                    # Componente raíz
│   ├── components/                # Componentes reutilizables
│   │   ├── ui/                    # UI primitivos (Headless UI)
│   │   │   ├── Button.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Select.tsx
│   │   │   └── ...
│   │   ├── CaseCard.tsx
│   │   ├── CaseTimeline.tsx 🆕   # Timeline visual
│   │   ├── ObservationEditor.tsx 🆕  # Editor de observaciones
│   │   ├── BulkActions.tsx 🆕    # Acciones masivas
│   │   └── ...
│   ├── pages/                     # Páginas/Vistas
│   │   ├── Dashboard.tsx          # Vista principal
│   │   ├── CaseForm.tsx           # Crear/editar caso
│   │   ├── CaseDetail.tsx 🆕     # Vista detallada con timeline
│   │   ├── ImportExport.tsx       # Import/Export module
│   │   ├── Users.tsx              # Gestión usuarios (ADMIN)
│   │   └── Login.tsx              # Autenticación
│   ├── context/                   # Context API
│   │   ├── AuthContext.tsx        # Estado de autenticación
│   │   └── ThemeContext.tsx       # Tema claro/oscuro
│   ├── api/                       # Cliente HTTP
│   │   ├── axiosConfig.ts         # Configuración Axios
│   │   ├── cases.ts               # Endpoints de casos
│   │   ├── users.ts               # Endpoints de usuarios
│   │   └── auth.ts                # Endpoints de auth
│   ├── types/                     # TypeScript types
│   │   ├── Case.ts
│   │   ├── User.ts
│   │   ├── Observation.ts 🆕
│   │   └── Audit.ts 🆕
│   ├── utils/                     # Utilidades
│   │   ├── dateFormat.ts
│   │   ├── permissions.ts 🆕     # Helper de permisos
│   │   └── validators.ts
│   ├── hooks/                     # Custom hooks
│   │   ├── useCases.ts
│   │   ├── useAuth.ts
│   │   ├── useTimeline.ts 🆕
│   │   └── useBulkUpdate.ts 🆕
│   └── test/                      # Tests frontend
│       ├── setup.ts
│       ├── mocks/
│       └── __tests__/
├── public/                        # Assets estáticos
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── vitest.config.ts
```

### Gestión de Estado

**React Query para Estado del Servidor**:

```typescript
// Ejemplo: Hook para obtener casos
export function useCases(filters: CaseFilters) {
  return useQuery({
    queryKey: ['cases', filters],
    queryFn: () => casesAPI.getAll(filters),
    staleTime: 30000, // 30 segundos
    cacheTime: 300000, // 5 minutos
  });
}

// Ejemplo: Mutation para bulk update 🆕
export function useBulkUpdate() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: BulkUpdatePayload) => casesAPI.bulkUpdate(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
      toast.success('Casos actualizados exitosamente');
    },
    onError: (error) => {
      toast.error('Error al actualizar casos');
    },
  });
}
```

**Context API para Estado Global**:

```typescript
// AuthContext
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  hasRole: (role: UserRole) => boolean; 🆕
  canEdit: (observation: Observation) => boolean; 🆕
}
```

### Componentes Nuevos v2.3.0 🆕

#### CaseTimeline.tsx
```typescript
interface TimelineEvent {
  type: 'CREATE' | 'OBSERVATION' | 'AUDIT';
  id: number;
  content?: string;
  action?: string;
  details?: Record<string, any>;
  created_at: string;
  user_name: string;
}

export function CaseTimeline({ caseId }: { caseId: number }) {
  const { data: timeline, isLoading } = useTimeline(caseId);
  
  return (
    <div className="space-y-4">
      {timeline?.map((event) => (
        <TimelineItem key={`${event.type}-${event.id}`} event={event} />
      ))}
    </div>
  );
}
```

#### ObservationEditor.tsx
```typescript
interface ObservationEditorProps {
  observation: Observation;
  onSave: (content: string) => Promise<void>;
  canEdit: boolean;
}

export function ObservationEditor({ observation, onSave, canEdit }: ObservationEditorProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [content, setContent] = useState(observation.content);
  
  // ... lógica de edición con control de permisos
}
```

---

## 🗄️ Base de Datos

### Esquema de Base de Datos

#### Tablas Principales

**user** (Usuarios):
```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('ADMIN', 'INGRESO', 'CONSULTA')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON user(email);
```

**case** (Casos):
```sql
CREATE TABLE "case" (  -- Escapado porque es palabra reservada
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('ABIERTO', 'STANDBY', 'EN_MONITOREO', 'CERRADO')),
    sby_responsable VARCHAR(100),
    servicio_o_plataforma VARCHAR(255) NOT NULL,
    prioridad VARCHAR(20) NOT NULL CHECK (prioridad IN ('CRITICO', 'ALTO', 'MEDIO', 'BAJO')),
    motivo TEXT NOT NULL,
    observaciones TEXT,  -- DEPRECATED
    creado_por_id INTEGER REFERENCES user(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_codigo ON "case"(codigo);
CREATE INDEX idx_case_estado ON "case"(estado);
CREATE INDEX idx_case_prioridad ON "case"(prioridad);
CREATE INDEX idx_case_updated_at ON "case"(updated_at);
```

**observation** 🆕 (Observaciones):
```sql
CREATE TABLE observation (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES "case"(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP,
    created_by_id INTEGER REFERENCES user(id)
);

CREATE INDEX idx_observation_case_id ON observation(case_id);
CREATE INDEX idx_observation_created_at ON observation(created_at);
```

**case_audit** 🆕 (Auditoría):
```sql
CREATE TABLE case_audit (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES "case"(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL CHECK (action IN ('CREATE', 'UPDATE', 'BULK_UPDATE', 'COMMENT', 'EVIDENCE', 'DELETE')),
    details JSONB DEFAULT '{}',
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_case_audit_case_id ON case_audit(case_id);
CREATE INDEX idx_case_audit_timestamp ON case_audit(timestamp);
CREATE INDEX idx_case_audit_action ON case_audit(action);
```

**attachment** (Archivos Adjuntos):
```sql
CREATE TABLE attachment (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    case_id INTEGER NOT NULL REFERENCES "case"(id) ON DELETE CASCADE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attachment_case_id ON attachment(case_id);
```

### Relaciones CASCADE 🆕

**Configuración Crítica**:
- Al eliminar un caso, se eliminan automáticamente:
  - Todas sus observaciones
  - Todos sus archivos adjuntos
  - Todo su historial de auditoría

```python
# En SQLModel
case_id: int = Field(foreign_key="case.id", ondelete="CASCADE")

# En Relationships
Relationship(sa_relationship_kwargs={"passive_deletes": True})
```

### Índices y Performance

**Índices Importantes**:
- `case.codigo`: Búsquedas por código (UNIQUE)
- `case.updated_at`: Ordenamiento y filtros por fecha
- `case.estado`: Filtros por estado
- `observation.case_id`: Join con casos
- `case_audit.case_id`: Timeline queries

**Queries Optimizadas**:
```python
# Uso de selectinload para evitar N+1
query = select(Case).where(Case.id == case_id).options(
    selectinload(Case.observaciones_list),
    selectinload(Case.attachments)
)
```

---

## 🔒 Autenticación y Seguridad

### JWT Authentication

**Configuración**:
```python
SECRET_KEY = os.getenv("SECRET_KEY")  # Mínimo 32 caracteres
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**Flujo de Autenticación**:
1. Usuario envía credenciales a `/auth/login`
2. Backend valida contra base de datos
3. Si válido, genera JWT con claims:
   ```json
   {
     "sub": "user@example.com",
     "rol": "ADMIN",
     "exp": 1706295600
   }
   ```
4. Frontend almacena token (localStorage/memory)
5. Todas las requests incluyen: `Authorization: Bearer <token>`

### Control de Acceso por Roles 🆕

**Matriz de Permisos**:

| Operación | CONSULTA | INGRESO | ADMIN |
|-----------|----------|---------|-------|
| Ver casos | ✅ | ✅ | ✅ |
| Crear casos | ❌ | ✅ | ✅ |
| Editar casos | ❌ | ✅ | ✅ |
| **Eliminar casos** 🆕 | ❌ | ❌ | ✅ |
| Editar propia observación 🆕 | ✅ | ✅ | ✅ |
| Editar cualquier observación 🆕 | ❌ | ✅ | ✅ |
| Bulk updates 🆕 | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ✅ |

**Implementación en Backend**:
```python
def require_role(allowed_roles: List[UserRole]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.rol not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

# Uso en endpoints
@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    # Solo ADMIN puede acceder
```

### Seguridad Adicional

**Password Hashing**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**SQL Injection Protection**:
- Uso de ORM parameterizado (SQLModel)
- Validación con Pydantic
- Sanitización de inputs

---

## 🆕 Nuevas Funcionalidades v2.3.0

### 1. Sistema de Eliminación Controlada

**Implementación**:
```python
@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Verificación de rol
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Solo ADMIN puede eliminar")
    
    db_case = await session.get(Case, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    case_codigo = db_case.codigo
    
    # DELETE con CASCADE automático
    await session.delete(db_case)
    await session.commit()
    
    return {
        "message": f"Caso {case_codigo} eliminado exitosamente",
        "deleted_case": {"id": case_id, "codigo": case_codigo}
    }
```

### 2. Edición de Observaciones con Permisos Granulares

**Control de Permisos**:
```python
@router.patch("/observations/{observation_id}")
async def update_observation(
    observation_id: int,
    observation_update: ObservationUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    obs = await session.get(Observation, observation_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observación no encontrada")
    
    # Control de permisos
    if current_user.rol not in [UserRole.INGRESO, UserRole.ADMIN]:
        # CONSULTA solo puede editar sus propias observaciones
        if obs.created_by_id != current_user.id:
            raise HTTPException(status_code=403, detail="No autorizado")
    
    obs.content = observation_update.content
    obs.edited_at = datetime.utcnow()
    
    await session.commit()
    return obs
```

### 3. Timeline Completo

**Endpoint**:
```python
@router.get("/{case_id}/timeline")
async def get_case_timeline(
    case_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Obtener caso
    case = await session.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    
    # Obtener observaciones con usuario
    obs_query = select(Observation).where(
        Observation.case_id == case_id
    ).options(selectinload(Observation.created_by))
    observations = (await session.execute(obs_query)).scalars().all()
    
    # Obtener auditorías con usuario
    audit_query = select(CaseAudit).where(
        CaseAudit.case_id == case_id
    ).options(selectinload(CaseAudit.user))
    audits = (await session.execute(audit_query)).scalars().all()
    
    # Construir timeline
    timeline = []
    
    # Evento de creación
    timeline.append({
        "type": "CREATE",
        "id": 0,
        "content": case.motivo,
        "created_at": case.created_at,
        "user_name": "Sistema"
    })
    
    # Observaciones
    for obs in observations:
        timeline.append({
            "type": "OBSERVATION",
            "id": obs.id,
            "content": obs.content,
            "created_at": obs.created_at,
            "user_name": obs.created_by.nombre if obs.created_by else "Usuario"
        })
    
    # Auditorías
    for audit in audits:
        timeline.append({
            "type": "AUDIT",
            "id": audit.id,
            "action": audit.action,
            "details": audit.details,
            "created_at": audit.timestamp,
            "user_name": audit.user.nombre if audit.user else "Sistema"
        })
    
    # Ordenar cronológicamente
    timeline.sort(key=lambda x: x["created_at"])
    
    return timeline
```

### 4. Bulk Updates con Auditoría

**Implementación**:
```python
@router.post("/bulk-update")
async def bulk_update_cases(
    payload: BulkUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.rol not in [UserRole.INGRESO, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    query = select(Case).where(Case.id.in_(payload.ids))
    cases = (await session.execute(query)).scalars().all()
    
    updated_count = 0
    
    for case in cases:
        audit_details = {}
        
        if payload.action == "CLOSE":
            if case.estado != CaseStatus.CERRADO:
                audit_details["estado"] = {
                    "old": case.estado,
                    "new": CaseStatus.CERRADO
                }
                case.estado = CaseStatus.CERRADO
        
        elif payload.action == "ASSIGN":
            if case.sby_responsable != payload.value:
                audit_details["sby_responsable"] = {
                    "old": case.sby_responsable,
                    "new": payload.value
                }
                case.sby_responsable = payload.value
        
        elif payload.action == "PRIORITY":
            new_priority = Priority(payload.value)
            if case.prioridad != new_priority:
                audit_details["prioridad"] = {
                    "old": case.prioridad,
                    "new": new_priority
                }
                case.prioridad = new_priority
        
        # Si hubo cambios, crear auditoría
        if audit_details:
            case.updated_at = datetime.utcnow()
            session.add(case)
            
            audit = CaseAudit(
                case_id=case.id,
                user_id=current_user.id,
                action=CaseAuditType.BULK_UPDATE,
                details=audit_details,
                timestamp=datetime.utcnow()
            )
            session.add(audit)
            updated_count += 1
    
    await session.commit()
    return {"message": f"Updated {updated_count} cases successfully"}
```

---

## 🧪 Testing

### Estructura de Tests

```
test/
├── conftest.py              # Fixtures compartidas
├── unit/                    # Tests unitarios (sin DB)
│   ├── test_auth_unit.py   # Tests de JWT, hashing
│   └── test_models.py      # Tests de validación Pydantic
└── integration/            # Tests de integración (con DB)
    ├── test_auth_integration.py      # Login, refresh
    ├── test_cases_integration.py     # CRUD casos + nuevas funcionalidades
    └── test_users_integration.py     # CRUD usuarios
```

### Cobertura de Tests v2.3.0

**Estadísticas**:
- Cobertura total: **92%**
- Total de pruebas: **67+**
- Tests nuevos v2.3.0: **21**

**Desglose por Módulo**:
| Módulo | Cobertura | Tests |
|--------|-----------|-------|
| `cases.py` | 95% | 40+ |
| `auth.py` | 92% | 12 |
| `users.py` | 90% | 10 |
| `models.py` | 88% | 8 |

**Nuevos Tests v2.3.0** 🆕:

1. **Tests de Eliminación** (6 pruebas):
   - DELETE por ADMIN
   - Permisos denegados para INGRESO/CONSULTA
   - CASCADE de observaciones/attachments/audits
   - Casos inexistentes

2. **Tests de Observaciones** (7 pruebas):
   - Editar observación propia
   - Permisos por rol
   - Actualización de `edited_at`
   - Observaciones inexistentes

3. **Tests de Bulk Updates** (4 pruebas):
   - Cerrar múltiples casos
   - Asignar responsable
   - Cambiar prioridad
   - Auditoría generada

4. **Tests de Timeline** (4 pruebas):
   - Timeline completo
   - Orden cronológico
   - Estructura de auditoría

### Ejecutar Tests

```bash
cd backend

# Todos los tests
pytest

# Solo unitarios
pytest test/unit -v

# Solo integración
pytest test/integration -v

# Con coverage
pytest --cov=app --cov-report=html

# Tests específicos
pytest test/integration/test_cases_integration.py::TestCaseDelete -v
```

Ver [backend/test/README.md](../backend/test/README.md) para guía completa.

---

## 🚀 Deployment

### Estrategia de Despliegue Productivo

**Para Producción: IMAGEN CON CÓDIGO** (NO volúmenes)

#### Dockerfile.prod (Backend)

```dockerfile
# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.10-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# ==========================================
# STAGE 2: Runtime
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de aplicación
COPY . .

# Crear directorio uploads
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    restart: unless-stopped

  redis:
    image: redis:alpine
    restart: unless-stopped

  backend:
    image: standby-backend:${VERSION:-latest}
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    # ❌ SIN VOLUMEN DE CÓDIGO
    volumes:
      - standby_uploads:/app/uploads  # Solo datos
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  frontend:
    image: standby-frontend:${VERSION:-latest}
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  standby_uploads:
```

### Build y Deploy

```bash
# Build con versión
docker build -f backend/Dockerfile.prod -t standby-backend:2.3.0 ./backend

# Tag para registry
docker tag standby-backend:2.3.0 yourregistry/standby-backend:2.3.0

# Push
docker push yourregistry/standby-backend:2.3.0

# Deploy en servidor
docker-compose -f docker-compose.prod.yml up -d
```

### Variables de Entorno Producción

```bash
# .env.prod (NO COMMITEAR)
DATABASE_URL=postgresql+asyncpg://prod_user:secure_pass@db:5432/prod_db
REDIS_URL=redis://redis:6379
SECRET_KEY=<32+ caracteres aleatorios>
ALLOWED_ORIGINS=https://yourdomain.com
```

---

## 📊 API Reference

Ver [API_REFERENCE.md](./API_REFERENCE.md) para documentación completa de todos los endpoints.

**Endpoints Principales**:

- **Auth**: `/auth/login`, `/auth/me`, `/auth/refresh`
- **Casos**: `/cases`, `/cases/{id}`, `/cases/bulk-update`, `/cases/{id}/timeline`
- **Observaciones**: `/cases/observations/{id}`
- **Usuarios**: `/users`, `/users/{id}`
- **Archivos**: `/files/upload`, `/files/download/{filename}`
- **Stats**: `/stats/dashboard`, `/stats/cases-by-status`
- **Import/Export**: `/cases-io/import-with-observations`, `/cases-io/export-with-observations`

---

## 📝 Notas Técnicas Adicionales

### Performance Optimization

1. **Query Optimization**:
   - Uso de índices en campos frecuentemente buscados
   - `selectinload` para evitar N+1 queries
   - Paginación en todas las listas

2. **Caching** (opcional con Redis):
   - Dashboard stats (TTL: 5 minutos)
   - User sessions
   - Query results frecuentes

3. **Async/Await**:
   - Todo el stack es asíncrono (FastAPI + asyncpg)
   - Non-blocking I/O para mejor concurrencia

### Escalabilidad

- **Horizontal**: Múltiples instancias detrás de load balancer
- **Vertical**: Aumentar workers de uvicorn
- **Database**: Connection pooling configurado
- **File Storage**: Migrar a S3/object storage en cloud

### Seguridad Adicional

- Rate limiting (con Redis)
- Input sanitization
- HTTPS en producción (Nginx/Traefik)
- Secrets management (Vault/AWS Secrets Manager)
- Database backups automáticos

---

**Versión de la Documentación**: 2.3.0  
**Última actualización**: Enero 26, 2026  
**Mantenido por**: Equipo de Desarrollo Standby Case Manager
