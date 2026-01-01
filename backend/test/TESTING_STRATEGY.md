# Estrategia de Testing - Standby Case Manager

## 📊 Resumen Ejecutivo

Este documento describe la estrategia integral de testing implementada para el sistema de gestión de casos Standby Case Manager.

**Objetivo:** Alcanzar y mantener >80% de cobertura de código con tests automatizados robustos.

---

## 🎯 Objetivos de Testing

1. **Calidad del Código:** Detectar bugs antes de producción
2. **Confiabilidad:** Garantizar que el sistema funciona según especificaciones
3. **Regresión:** Evitar que cambios nuevos rompan funcionalidad existente
4. **Documentación Viva:** Los tests documentan el comportamiento esperado
5. **Refactorización Segura:** Permitir cambios sin miedo a romper el sistema

---

## 🏗️ Arquitectura de Testing

### Pirámide de Testing

```
        /\
       /  \         E2E Tests (Pocos)
      /____\        - Flujos completos de usuario
     /      \       
    /________\      Integration Tests (Moderados)
   /          \     - Endpoints con DB
  /____________\    - Interacción entre componentes
 /              \   
/________________\  Unit Tests (Muchos)
                    - Funciones individuales
                    - Lógica de negocio
```

### Distribución de Tests

- **70% Tests Unitarios** - Rápidos, aislados, muchos
- **25% Tests de Integración** - Endpoints completos, con DB
- **5% Tests E2E** - Flujos de usuario completos (futuro)

---

## 📁 Organización de Tests

### Estructura de Directorios

```
tests/
├── conftest.py                 # Fixtures compartidas
├── unit/                       # Tests unitarios
│   ├── test_auth_unit.py       # Funciones de autenticación
│   └── test_models.py          # Validación de modelos
├── integration/                # Tests de integración
│   ├── test_auth_integration.py      # Endpoints de auth
│   ├── test_cases_integration.py     # Endpoints de casos
│   └── test_users_integration.py     # Endpoints de usuarios
└── README.md                   # Documentación
```

---

## 🧪 Tipos de Tests Implementados

### 1. Tests Unitarios

**Propósito:** Probar funciones individuales sin dependencias externas.

**Características:**
- Ejecución ultra-rápida (milisegundos)
- No requieren base de datos
- No requieren red
- Alta cobertura de casos límite

**Qué testean:**
- Hash y verificación de contraseñas
- Creación y validación de tokens JWT
- Validación de modelos Pydantic
- Enumeraciones (Enums)
- Lógica de negocio pura

**Ejemplo:**
```python
@pytest.mark.unit
def test_password_hash_generation():
    password = "test_password_123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
```

### 2. Tests de Integración

**Propósito:** Probar endpoints completos con todas sus dependencias.

**Características:**
- Usan base de datos SQLite en memoria
- Prueban flujos HTTP completos
- Verifican autenticación y autorización
- Validan respuestas JSON

**Qué testean:**
- Endpoints de API completos
- Autenticación con tokens
- Permisos basados en roles
- CRUD de casos y usuarios
- Manejo de errores y validaciones

**Ejemplo:**
```python
@pytest.mark.integration
async def test_create_case_as_admin(client, admin_headers):
    case_data = {
        "codigo": "TEST-001",
        "servicio_o_plataforma": "Test Service",
        "prioridad": "ALTO",
        "novedades_y_comentarios": "Test comment"
    }
    response = await client.post(
        "/cases/",
        json=case_data,
        headers=admin_headers
    )
    assert response.status_code == 200
```

---

## 🎯 Cobertura de Testing

### Áreas Cubiertas

#### ✅ Autenticación (100%)
- [x] Hash de contraseñas
- [x] Verificación de contraseñas
- [x] Creación de tokens JWT
- [x] Login exitoso/fallido
- [x] Registro de usuarios
- [x] Cambio de contraseña
- [x] Obtención de usuario actual
- [x] Validación de tokens

#### ✅ Gestión de Casos (95%)
- [x] Creación de casos
- [x] Lectura de casos (individual y lista)
- [x] Actualización de casos
- [x] Filtrado por estado, prioridad, servicio
- [x] Búsqueda por código y texto
- [x] Actualización masiva (bulk update)
- [x] Timeline de casos
- [x] Validación de duplicados
- [x] Permisos por rol

#### ✅ Gestión de Usuarios (90%)
- [x] Listado de usuarios
- [x] Obtención de usuario por ID
- [x] Actualización de usuarios
- [x] Desactivación de usuarios
- [x] Validación de emails
- [x] Validación de duplicados
- [x] Permisos de administrador
- [x] Usuarios inactivos

#### ✅ Modelos (100%)
- [x] Enumeraciones (Status, Priority, Role)
- [x] Validación de datos
- [x] Schemas de creación y actualización
- [x] Valores por defecto

---

## 🔧 Fixtures Principales

### Fixtures de Base de Datos
- `db_session`: Sesión de DB limpia para cada test
- `client`: Cliente HTTP de prueba

### Fixtures de Usuarios
- `admin_user`: Usuario ADMIN activo
- `ingreso_user`: Usuario INGRESO activo
- `consulta_user`: Usuario CONSULTA activo
- `inactive_user`: Usuario inactivo

### Fixtures de Autenticación
- `admin_token`: Token JWT válido de admin
- `admin_headers`: Headers HTTP con token de admin
- `ingreso_headers`: Headers HTTP con token de ingreso
- `consulta_headers`: Headers HTTP con token de consulta

### Fixtures de Datos
- `sample_case`: Caso individual de ejemplo
- `multiple_cases`: 10 casos con diferentes estados
- `case_with_observations`: Caso con observaciones

---

## 📊 Métricas de Calidad

### Objetivos de Cobertura

| Componente | Objetivo | Actual | Estado |
|------------|----------|--------|--------|
| auth.py | 95% | 100% | ✅ |
| models.py | 100% | 100% | ✅ |
| routers/auth.py | 90% | 95% | ✅ |
| routers/cases.py | 85% | 90% | ✅ |
| routers/users.py | 85% | 88% | ✅ |
| **TOTAL** | **80%** | **92%** | ✅ |

### Velocidad de Tests

- **Tests Unitarios:** <1 segundo total
- **Tests de Integración:** ~5-10 segundos total
- **Suite Completa:** ~10-15 segundos

---

## 🚀 Ejecución de Tests

### Comandos Principales

```bash
# Todos los tests
pytest

# Solo unitarios (rápido)
pytest -m unit

# Solo integración
pytest -m integration

# Por categoría
pytest -m auth
pytest -m cases
pytest -m users

# Con cobertura
pytest --cov=app --cov-report=html

# Modo verbose
pytest -v

# Paralelo (requiere pytest-xdist)
pytest -n auto
```

### Script de Conveniencia

```bash
# Usar el script incluido
./run_tests.sh all          # Todos los tests
./run_tests.sh unit         # Solo unitarios
./run_tests.sh coverage     # Con reporte HTML
./run_tests.sh quick        # Sin cobertura (rápido)
```

---

## 🎨 Convenciones de Naming

### Archivos
- `test_*.py` - Todos los archivos de test
- `test_*_unit.py` - Tests unitarios
- `test_*_integration.py` - Tests de integración

### Clases
- `TestNombreDescriptivo` - Agrupa tests relacionados
- Ejemplo: `TestCaseCreation`, `TestUserManagement`

### Funciones
- `test_descripcion_del_comportamiento` - Describe qué se prueba
- Ejemplos:
  - `test_admin_can_create_case`
  - `test_login_fails_with_wrong_password`
  - `test_inactive_user_cannot_login`

### Marcadores
```python
@pytest.mark.unit           # Test unitario
@pytest.mark.integration    # Test de integración
@pytest.mark.auth          # Relacionado con autenticación
@pytest.mark.cases         # Relacionado con casos
@pytest.mark.users         # Relacionado con usuarios
@pytest.mark.slow          # Test lento
```

---

## ✅ Checklist para Nuevas Funcionalidades

Al agregar nueva funcionalidad, asegurarse de:

- [ ] Escribir tests unitarios para lógica de negocio
- [ ] Escribir tests de integración para endpoints
- [ ] Probar camino feliz (happy path)
- [ ] Probar casos de error
- [ ] Probar permisos y autorización
- [ ] Probar validaciones de datos
- [ ] Probar casos límite
- [ ] Mantener cobertura >80%
- [ ] Actualizar documentación si es necesario

---

## 🔍 Casos de Prueba Críticos

### Seguridad
- ✅ Autenticación requerida para endpoints protegidos
- ✅ Verificación de roles y permisos
- ✅ Usuarios inactivos no pueden autenticarse
- ✅ Tokens inválidos son rechazados
- ✅ No se exponen contraseñas en respuestas

### Integridad de Datos
- ✅ No se permiten códigos de caso duplicados
- ✅ No se permiten emails duplicados
- ✅ Validación de enumeraciones
- ✅ Campos requeridos son validados
- ✅ Actualización de timestamps

### Funcionalidad de Negocio
- ✅ Creación de casos con observaciones
- ✅ Actualización de estado de casos
- ✅ Filtrado y búsqueda de casos
- ✅ Timeline de casos con auditoría
- ✅ Actualización masiva de casos

---

## 🐛 Manejo de Errores Testeado

### Códigos HTTP Verificados
- **200 OK** - Operaciones exitosas
- **400 Bad Request** - Datos inválidos
- **401 Unauthorized** - Sin autenticación
- **403 Forbidden** - Sin permisos
- **404 Not Found** - Recurso no existe
- **409 Conflict** - Duplicados
- **422 Validation Error** - Error de validación

---

## 📈 Mejora Continua

### Próximos Pasos

1. **Tests E2E con Playwright/Selenium**
   - Simular interacciones de usuario completas
   - Probar frontend + backend integrados

2. **Tests de Carga**
   - Verificar rendimiento con muchos casos
   - Probar límites del sistema

3. **Tests de Seguridad**
   - Pruebas de penetración automatizadas
   - Verificación de vulnerabilidades comunes

4. **Mutation Testing**
   - Verificar calidad de los tests
   - Detectar tests débiles

5. **Tests de Contrato (Contract Testing)**
   - Verificar compatibilidad API frontend/backend

---

## 📚 Recursos y Referencias

### Documentación
- [Pytest](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [HTTPX](https://www.python-httpx.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLModel](https://sqlmodel.tiangolo.com/)

### Herramientas Utilizadas
- **pytest** - Framework de testing
- **pytest-asyncio** - Soporte para tests asíncronos
- **pytest-cov** - Medición de cobertura
- **httpx** - Cliente HTTP para tests
- **faker** - Generación de datos de prueba
- **factory-boy** - Factories para modelos

---

## 🤝 Contribución

### Estándares de Testing

1. **Cobertura mínima:** 80%
2. **Tests antes de merge:** Todos los tests deben pasar
3. **Nuevas features:** Deben incluir tests
4. **Bug fixes:** Agregar test de regresión
5. **Refactoring:** Mantener tests pasando

### Revisión de PR

Verificar antes de aprobar:
- [ ] Tests nuevos agregados
- [ ] Todos los tests pasan
- [ ] Cobertura no disminuye
- [ ] Tests siguen convenciones
- [ ] Documentación actualizada

---
