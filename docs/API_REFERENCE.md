# 📚 API Reference - Standby Case Manager

Documentación completa de todos los endpoints de la API REST.

**Base URL**: `http://localhost:8000`  
**API Version**: v2.3.0  
**Authentication**: JWT Bearer Token

---

## 📋 Tabla de Contenidos

1. [Autenticación](#-autenticación)
2. [Casos](#-casos)
3. [Observaciones](#-observaciones)
4. [Operaciones Masivas](#-operaciones-masivas)
5. [Timeline y Auditoría](#-timeline-y-auditoría)
6. [Usuarios](#-usuarios)
7. [Archivos](#-archivos)
8. [Estadísticas](#-estadísticas)
9. [Import/Export](#-importexport)
10. [Códigos de Estado](#-códigos-de-estado)
11. [Modelos de Datos](#-modelos-de-datos)

---

## 🔐 Autenticación

Todos los endpoints (excepto `/auth/login`) requieren autenticación mediante JWT Bearer Token.

### Header de Autenticación

```http
Authorization: Bearer <access_token>
```

### POST /auth/login

Iniciar sesión y obtener tokens de acceso.

**Request Body**:
```json
{
  "username": "admin@standby.com",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre": "Administrator",
    "email": "admin@standby.com",
    "rol": "ADMIN",
    "is_active": true
  }
}
```

**Errores**:
- `401 Unauthorized`: Credenciales inválidas
- `422 Unprocessable Entity`: Formato de request inválido

---

### GET /auth/me

Obtener información del usuario autenticado actual.

**Headers**:
```http
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "nombre": "Administrator",
  "email": "admin@standby.com",
  "rol": "ADMIN",
  "is_active": true
}
```

**Errores**:
- `401 Unauthorized`: Token inválido o expirado

---

### POST /auth/refresh

Renovar access token usando refresh token.

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 📦 Casos

### GET /cases

Listar casos con filtros y paginación.

**Query Parameters**:

| Parámetro | Tipo | Requerido | Descripción | Default |
|-----------|------|-----------|-------------|---------|
| `skip` | integer | No | Offset para paginación | 0 |
| `limit` | integer | No | Límite de resultados | 100 |
| `status` | string | No | Filtro por estado: `ABIERTO`, `STANDBY`, `EN_MONITOREO`, `CERRADO` | - |
| `priority` | string | No | Filtro por prioridad: `CRITICO`, `ALTO`, `MEDIO`, `BAJO` | - |
| `service` | string | No | Filtro por servicio/plataforma (búsqueda parcial) | - |
| `sby_responsable` | string | No | Filtro por responsable SBY (búsqueda parcial) | - |
| `search` | string | No | Búsqueda en código y motivo | - |
| `start_date` | datetime | No | Fecha inicio (ISO 8601) | - |
| `end_date` | datetime | No | Fecha fin (ISO 8601) | - |
| `timezone_offset` | integer | No | Offset de zona horaria en minutos | - |

**Example Request**:
```http
GET /cases?skip=0&limit=20&status=ABIERTO&priority=CRITICO&search=VPN
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "codigo": "CASE-001",
      "fecha_inicio": "2026-01-26T10:00:00Z",
      "fecha_fin": null,
      "estado": "ABIERTO",
      "sby_responsable": "Juan Pérez",
      "servicio_o_plataforma": "VPN Corporativa",
      "prioridad": "CRITICO",
      "motivo": "Falla en autenticación VPN",
      "observaciones": null,
      "creado_por_id": 1,
      "created_at": "2026-01-26T10:00:00Z",
      "updated_at": "2026-01-26T10:00:00Z"
    }
  ],
  "total": 45,
  "skip": 0,
  "limit": 20,
  "page": 1,
  "total_pages": 3
}
```

**Permisos**: Todos los roles

---

### POST /cases

Crear un nuevo caso.

**Request Body**:
```json
{
  "codigo": "CASE-123",
  "servicio_o_plataforma": "Servidor Web",
  "prioridad": "ALTO",
  "motivo": "Servidor no responde",
  "observaciones": "Observación inicial del caso",
  "sby_responsable": "María García"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "codigo": "CASE-123",
  "fecha_inicio": "2026-01-26T15:30:00Z",
  "fecha_fin": null,
  "estado": "ABIERTO",
  "sby_responsable": "María García",
  "servicio_o_plataforma": "Servidor Web",
  "prioridad": "ALTO",
  "motivo": "Servidor no responde",
  "observaciones": null,
  "creado_por_id": 2,
  "created_at": "2026-01-26T15:30:00Z",
  "updated_at": "2026-01-26T15:30:00Z"
}
```

**Notas**:
- Si se proporciona `observaciones`, se crea automáticamente en la tabla Observation
- El campo `observaciones` en el caso se establece en `null` (deprecado)
- El estado inicial es siempre `ABIERTO`

**Errores**:
- `400 Bad Request`: Código de caso ya existe
- `403 Forbidden`: Usuario no tiene permisos (debe ser INGRESO o ADMIN)
- `422 Unprocessable Entity`: Datos inválidos

**Permisos**: INGRESO, ADMIN

---

### GET /cases/{case_id}

Obtener un caso específico con todas sus observaciones y attachments.

**Path Parameters**:
- `case_id` (integer): ID del caso

**Response** (200 OK):
```json
{
  "id": 1,
  "codigo": "CASE-001",
  "fecha_inicio": "2026-01-26T10:00:00Z",
  "fecha_fin": null,
  "estado": "ABIERTO",
  "sby_responsable": "Juan Pérez",
  "servicio_o_plataforma": "VPN Corporativa",
  "prioridad": "CRITICO",
  "motivo": "Falla en autenticación VPN",
  "observaciones": null,
  "creado_por_id": 1,
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T10:00:00Z",
  "observaciones_list": [
    {
      "id": 1,
      "content": "Observación inicial del caso",
      "created_at": "2026-01-26T10:00:00Z",
      "edited_at": null,
      "created_by_id": 1,
      "case_id": 1
    },
    {
      "id": 2,
      "content": "Se identificó problema en servidor RADIUS",
      "created_at": "2026-01-26T11:30:00Z",
      "edited_at": "2026-01-26T12:00:00Z",
      "created_by_id": 2,
      "case_id": 1
    }
  ],
  "attachments": [
    {
      "id": 1,
      "filename": "error_log.txt",
      "file_path": "/uploads/caso_1_error_log.txt",
      "file_size": 15360,
      "content_type": "text/plain",
      "uploaded_at": "2026-01-26T10:15:00Z"
    }
  ]
}
```

**Errores**:
- `404 Not Found`: Caso no existe

**Permisos**: Todos los roles

---

### PATCH /cases/{case_id}

Actualizar un caso existente.

**Path Parameters**:
- `case_id` (integer): ID del caso

**Request Body** (todos los campos opcionales):
```json
{
  "codigo": "CASE-123-UPD",
  "servicio_o_plataforma": "Servidor Web Prod",
  "prioridad": "CRITICO",
  "estado": "EN_MONITOREO",
  "sby_responsable": "Carlos Rodríguez",
  "motivo": "Servidor no responde - actualizado",
  "observaciones": "Nueva observación agregada",
  "fecha_fin": "2026-01-26T18:00:00Z"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "codigo": "CASE-123-UPD",
  "fecha_inicio": "2026-01-26T15:30:00Z",
  "fecha_fin": "2026-01-26T18:00:00Z",
  "estado": "EN_MONITOREO",
  "sby_responsable": "Carlos Rodríguez",
  "servicio_o_plataforma": "Servidor Web Prod",
  "prioridad": "CRITICO",
  "motivo": "Servidor no responde - actualizado",
  "observaciones": null,
  "creado_por_id": 2,
  "created_at": "2026-01-26T15:30:00Z",
  "updated_at": "2026-01-26T18:05:00Z"
}
```

**Notas**:
- Si se proporciona `observaciones`, se crea como nueva entrada en Observation
- Se genera automáticamente un registro de auditoría con los cambios
- Solo se auditan campos que realmente cambiaron

**Errores**:
- `403 Forbidden`: Usuario no tiene permisos (debe ser INGRESO o ADMIN)
- `404 Not Found`: Caso no existe

**Permisos**: INGRESO, ADMIN

---

### DELETE /cases/{case_id} 🆕

Eliminar un caso y todas sus relaciones (CASCADE).

**Path Parameters**:
- `case_id` (integer): ID del caso

**Response** (200 OK):
```json
{
  "message": "Caso CASE-123 eliminado exitosamente",
  "deleted_case": {
    "id": 10,
    "codigo": "CASE-123"
  }
}
```

**Notas**:
- Elimina automáticamente todas las observaciones del caso
- Elimina automáticamente todos los attachments del caso
- Elimina automáticamente todos los registros de auditoría del caso
- Esta operación es **irreversible**

**Errores**:
- `403 Forbidden`: Usuario no es ADMIN
- `404 Not Found`: Caso no existe

**Permisos**: SOLO ADMIN

---

## 📝 Observaciones

### PATCH /cases/observations/{observation_id} 🆕

Editar una observación existente.

**Path Parameters**:
- `observation_id` (integer): ID de la observación

**Request Body**:
```json
{
  "content": "Contenido actualizado de la observación"
}
```

**Response** (200 OK):
```json
{
  "id": 5,
  "content": "Contenido actualizado de la observación",
  "created_at": "2026-01-26T10:00:00Z",
  "edited_at": "2026-01-26T14:30:00Z",
  "created_by_id": 2,
  "case_id": 1
}
```

**Control de Permisos**:
- **CONSULTA**: Solo puede editar sus propias observaciones
- **INGRESO**: Puede editar cualquier observación
- **ADMIN**: Puede editar cualquier observación

**Errores**:
- `403 Forbidden`: Usuario no tiene permisos para editar esta observación
- `404 Not Found`: Observación no existe

**Permisos**: Todos (con restricciones según rol)

---

## ⚡ Operaciones Masivas

### POST /cases/bulk-update 🆕

Actualizar múltiples casos simultáneamente.

**Request Body**:
```json
{
  "ids": [1, 2, 3, 4, 5],
  "action": "CLOSE",
  "value": "CERRADO"
}
```

**Acciones Disponibles**:

| Action | Value | Descripción |
|--------|-------|-------------|
| `CLOSE` | `"CERRADO"` | Cerrar los casos seleccionados |
| `ASSIGN` | `"Nombre del Responsable"` | Asignar responsable masivamente |
| `PRIORITY` | `"CRITICO"`, `"ALTO"`, `"MEDIO"`, `"BAJO"` | Cambiar prioridad |

**Example - Cerrar casos**:
```json
{
  "ids": [10, 15, 20],
  "action": "CLOSE",
  "value": "CERRADO"
}
```

**Example - Asignar responsable**:
```json
{
  "ids": [5, 6, 7],
  "action": "ASSIGN",
  "value": "Pedro Martínez"
}
```

**Example - Cambiar prioridad**:
```json
{
  "ids": [1, 2],
  "action": "PRIORITY",
  "value": "CRITICO"
}
```

**Response** (200 OK):
```json
{
  "message": "Updated 5 cases successfully"
}
```

**Notas**:
- Solo actualiza casos que realmente cambian (evita actualizaciones innecesarias)
- Genera un registro de auditoría (`BULK_UPDATE`) por cada caso actualizado
- Actualiza automáticamente el campo `updated_at`

**Errores**:
- `403 Forbidden`: Usuario no tiene permisos (debe ser INGRESO o ADMIN)
- `422 Unprocessable Entity`: Acción inválida o IDs vacíos

**Permisos**: INGRESO, ADMIN

---

## 🕒 Timeline y Auditoría

### GET /cases/{case_id}/timeline 🆕

Obtener el timeline completo de un caso con todos los eventos.

**Path Parameters**:
- `case_id` (integer): ID del caso

**Response** (200 OK):
```json
[
  {
    "type": "CREATE",
    "id": 0,
    "action": "CREATE",
    "content": "Falla en autenticación VPN",
    "created_at": "2026-01-26T10:00:00Z",
    "user_id": 1,
    "user_name": "Administrator",
    "details": {
      "servicio": "VPN Corporativa",
      "prioridad": "CRITICO",
      "sby_responsable": "Juan Pérez"
    }
  },
  {
    "type": "OBSERVATION",
    "id": 1,
    "content": "Se identificó problema en servidor RADIUS",
    "created_at": "2026-01-26T11:30:00Z",
    "user_id": 2,
    "user_name": "Operador Ingreso"
  },
  {
    "type": "AUDIT",
    "id": 1,
    "action": "UPDATE",
    "details": {
      "estado": {
        "old": "ABIERTO",
        "new": "EN_MONITOREO"
      },
      "prioridad": {
        "old": "ALTO",
        "new": "CRITICO"
      }
    },
    "created_at": "2026-01-26T12:00:00Z",
    "user_name": "Administrator"
  },
  {
    "type": "AUDIT",
    "id": 2,
    "action": "BULK_UPDATE",
    "details": {
      "estado": {
        "old": "EN_MONITOREO",
        "new": "CERRADO"
      }
    },
    "created_at": "2026-01-26T18:00:00Z",
    "user_name": "Administrator"
  }
]
```

**Tipos de Eventos**:

1. **CREATE**: Creación del caso
   - Incluye motivo inicial y detalles del caso
   - Información del usuario creador

2. **OBSERVATION**: Nueva observación
   - Contenido de la observación
   - Usuario que la creó

3. **AUDIT**: Cambios en el caso
   - Actions posibles: `UPDATE`, `BULK_UPDATE`, `COMMENT`, `EVIDENCE`, `DELETE`
   - Detalles de cambios (old/new values)
   - Usuario que realizó el cambio

**Ordenamiento**: Cronológico ascendente (más antiguo primero)

**Errores**:
- `404 Not Found`: Caso no existe

**Permisos**: Todos los roles

---

## 👥 Usuarios

### GET /users

Listar todos los usuarios.

**Query Parameters**:
- `skip` (integer, default: 0): Offset para paginación
- `limit` (integer, default: 100): Límite de resultados

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "nombre": "Administrator",
    "email": "admin@standby.com",
    "rol": "ADMIN",
    "is_active": true
  },
  {
    "id": 2,
    "nombre": "Operador Ingreso",
    "email": "ingreso@standby.com",
    "rol": "INGRESO",
    "is_active": true
  }
]
```

**Permisos**: ADMIN

---

### POST /users

Crear un nuevo usuario.

**Request Body**:
```json
{
  "nombre": "Nuevo Usuario",
  "email": "nuevo@standby.com",
  "password": "password123",
  "rol": "CONSULTA"
}
```

**Response** (200 OK):
```json
{
  "id": 10,
  "nombre": "Nuevo Usuario",
  "email": "nuevo@standby.com",
  "rol": "CONSULTA",
  "is_active": true
}
```

**Errores**:
- `400 Bad Request`: Email ya existe

**Permisos**: ADMIN

---

### GET /users/{user_id}

Obtener un usuario específico.

**Response** (200 OK):
```json
{
  "id": 5,
  "nombre": "Usuario Consulta",
  "email": "consulta@standby.com",
  "rol": "CONSULTA",
  "is_active": true
}
```

**Permisos**: ADMIN o el propio usuario

---

### PATCH /users/{user_id}

Actualizar un usuario.

**Request Body** (todos los campos opcionales):
```json
{
  "nombre": "Nombre Actualizado",
  "email": "nuevo_email@standby.com",
  "password": "nueva_password",
  "rol": "INGRESO",
  "is_active": false
}
```

**Response** (200 OK):
```json
{
  "id": 5,
  "nombre": "Nombre Actualizado",
  "email": "nuevo_email@standby.com",
  "rol": "INGRESO",
  "is_active": false
}
```

**Permisos**: ADMIN o el propio usuario (con restricciones)

---

### DELETE /users/{user_id}

Eliminar un usuario.

**Response** (200 OK):
```json
{
  "message": "Usuario eliminado exitosamente",
  "deleted_user": {
    "id": 10,
    "email": "usuario@standby.com"
  }
}
```

**Permisos**: ADMIN

---

## 📁 Archivos

### POST /files/upload

Subir un archivo adjunto a un caso.

**Request** (multipart/form-data):
```
file: <binary>
case_id: 5
```

**Response** (200 OK):
```json
{
  "id": 15,
  "filename": "evidencia.png",
  "file_path": "/uploads/caso_5_evidencia.png",
  "file_size": 245760,
  "content_type": "image/png",
  "uploaded_at": "2026-01-26T15:00:00Z",
  "case_id": 5
}
```

**Tipos de Archivo Permitidos**:
- Imágenes: png, jpg, jpeg, gif
- Documentos: pdf, doc, docx, txt
- Logs: log, txt

**Límite de Tamaño**: 10 MB

**Permisos**: INGRESO, ADMIN

---

### GET /files/download/{filename}

Descargar un archivo.

**Response**: Binary file stream

**Permisos**: Todos los roles

---

### DELETE /files/{file_id}

Eliminar un archivo.

**Response** (200 OK):
```json
{
  "message": "Archivo eliminado exitosamente"
}
```

**Permisos**: INGRESO, ADMIN

---

## 📊 Estadísticas

### GET /stats/dashboard

Obtener métricas generales del dashboard.

**Response** (200 OK):
```json
{
  "total_cases": 150,
  "open_cases": 45,
  "standby_cases": 20,
  "monitoring_cases": 30,
  "closed_cases": 55,
  "critical_priority": 15,
  "high_priority": 40,
  "medium_priority": 60,
  "low_priority": 35,
  "last_updated": "2026-01-26T16:00:00Z"
}
```

**Permisos**: Todos los roles

---

### GET /stats/cases-by-status

Distribución de casos por estado.

**Response** (200 OK):
```json
[
  {
    "estado": "ABIERTO",
    "count": 45
  },
  {
    "estado": "STANDBY",
    "count": 20
  },
  {
    "estado": "EN_MONITOREO",
    "count": 30
  },
  {
    "estado": "CERRADO",
    "count": 55
  }
]
```

---

### GET /stats/cases-by-priority

Distribución de casos por prioridad.

**Response** (200 OK):
```json
[
  {
    "prioridad": "CRITICO",
    "count": 15
  },
  {
    "prioridad": "ALTO",
    "count": 40
  },
  {
    "prioridad": "MEDIO",
    "count": 60
  },
  {
    "prioridad": "BAJO",
    "count": 35
  }
]
```

---

## 📤 Import/Export

### POST /cases-io/import-with-observations

Importar casos con múltiples observaciones desde Excel/CSV.

**Request** (multipart/form-data):
```
file: <binary excel/csv>
```

**Formato del Archivo**:
- Cada fila = un caso
- Columnas requeridas:
  - `codigo`: Código único del caso
  - `servicio_o_plataforma`: Servicio/plataforma afectada
  - `prioridad`: CRITICO, ALTO, MEDIO, BAJO
  - `motivo`: Descripción del caso
  - `observaciones`: Observaciones separadas por `|`

**Response** (200 OK):
```json
{
  "imported_cases": 25,
  "total_observations": 78,
  "errors": []
}
```

---

### GET /cases-io/export-with-observations

Exportar casos con todas sus observaciones.

**Query Parameters**:
- `format` (string): `xlsx`, `csv` (default: `xlsx`)

**Response**: File download (Excel o CSV)

---

## 🔢 Códigos de Estado

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Operación exitosa sin contenido de respuesta |
| 400 | Bad Request | Request inválido o datos incorrectos |
| 401 | Unauthorized | Autenticación requerida o token inválido |
| 403 | Forbidden | No tiene permisos para esta operación |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Validación de datos falló |
| 500 | Internal Server Error | Error del servidor |

---

## 📦 Modelos de Datos

### CaseStatus (Enum)
```python
ABIERTO = "ABIERTO"
STANDBY = "STANDBY"
EN_MONITOREO = "EN_MONITOREO"
CERRADO = "CERRADO"
```

### Priority (Enum)
```python
CRITICO = "CRITICO"
ALTO = "ALTO"
MEDIO = "MEDIO"
BAJO = "BAJO"
```

### UserRole (Enum)
```python
ADMIN = "ADMIN"       # Control total
INGRESO = "INGRESO"   # Crear/editar casos
CONSULTA = "CONSULTA" # Solo lectura
```

### CaseAuditType (Enum)
```python
CREATE = "CREATE"
UPDATE = "UPDATE"
BULK_UPDATE = "BULK_UPDATE"
COMMENT = "COMMENT"
EVIDENCE = "EVIDENCE"
DELETE = "DELETE"
```

---

## 📝 Notas Adicionales

### Zona Horaria
- Todas las fechas se manejan en UTC (ISO 8601)
- El cliente debe convertir a zona horaria local
- El parámetro `timezone_offset` en búsquedas permite ajustar filtros

### Rate Limiting
- Actualmente no implementado
- Planificado para versión futura con Redis

### Versionado API
- Versión actual: v2.3.0
- Breaking changes solo en versiones MAJOR
- Deprecations anunciadas con 2 versiones de anticipación

---

**Última actualización**: 2026-01-26  
**Versión API**: 2.3.0
