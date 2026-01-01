# Guía de Testing - Standby Case Manager Backend

Esta guía documenta la estrategia de testing del backend del sistema de gestión de casos.

## 📋 Tabla de Contenidos

- [Estructura de Tests](#estructura-de-tests)
- [Configuración](#configuración)
- [Ejecución de Tests](#ejecución-de-tests)
- [Cobertura](#cobertura)
- [Tipos de Tests](#tipos-de-tests)
- [Fixtures Disponibles](#fixtures-disponibles)
- [Buenas Prácticas](#buenas-prácticas)
- [Troubleshooting](#troubleshooting)

---

## 📁 Estructura de Tests

```
backend/
├── test/                        # ⚠️ Nota: es 'test' sin 's'
│   ├── conftest.py              # Fixtures compartidas
│   ├── unit/                    # Tests unitarios
│   │   ├── test_auth_unit.py    # Tests de autenticación
│   │   └── test_models.py       # Tests de modelos
│   └── integration/             # Tests de integración
│       ├── test_auth_integration.py
│       ├── test_cases_integration.py
│       └── test_users_integration.py
├── pytest.ini                   # Configuración de pytest
├── requirements.txt             # Dependencias principales
└── requirements-test.txt        # Dependencias de testing
```

---

## ⚙️ Configuración

### 1. Crear Entorno Virtual

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias de testing
pip install -r requirements-test.txt
```

**Contenido de `requirements-test.txt`:**

```txt
# Testing Framework
pytest==8.0.0
pytest-asyncio==0.23.0
pytest-cov==4.1.0
pytest-xdist==3.5.0

# HTTP Testing
httpx==0.26.0

# Mocking
pytest-mock==3.12.0

# Database Testing
sqlalchemy-utils==0.41.1
```

### 3. Configuración de Pytest

El archivo `pytest.ini` configura el comportamiento de pytest:

```ini
[pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto

# Markers
markers =
    unit: Tests unitarios
    integration: Tests de integración
    auth: Tests de autenticación
    cases: Tests de casos
    users: Tests de usuarios
    slow: Tests que toman más tiempo

# Coverage
addopts = 
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
    -v
```

---

## 🚀 Ejecución de Tests

### Comandos Básicos

```bash
# Activar entorno virtual (si no está activo)
source .venv/bin/activate

# Ejecutar todos los tests
pytest

# Modo verbose (más detalles)
pytest -v

# Modo muy verbose (máximo detalle)
pytest -vv

# Ver output de print statements
pytest -s
```

### Tests por Tipo

```bash
# Solo tests unitarios
pytest test/unit -v

# Solo tests de integración
pytest test/integration -v

# Tests por marca
pytest -m unit          # Solo unitarios
pytest -m integration   # Solo integración
pytest -m auth          # Solo autenticación
pytest -m cases         # Solo casos
```

### Tests Específicos

```bash
# Ejecutar un archivo específico
pytest test/unit/test_auth_unit.py

# Ejecutar un archivo con verbose
pytest test/integration/test_cases_integration.py -v

# Ejecutar una clase específica
pytest test/unit/test_auth_unit.py::TestPasswordHashing

# Ejecutar un test específico
pytest test/unit/test_auth_unit.py::TestPasswordHashing::test_password_hash_generation
```

### Filtrar por Nombre

```bash
# Ejecutar tests que contengan "login" en el nombre
pytest -k "login"

# Ejecutar tests que NO contengan "slow"
pytest -k "not slow"

# Combinar filtros
pytest -k "login and not integration"
```

### Tests en Paralelo (Más Rápido)

```bash
# Usar todos los CPUs disponibles
pytest -n auto

# Usar 4 procesos
pytest -n 4
```

---

## 📊 Cobertura

### Generar Reporte de Cobertura

```bash
# Reporte en terminal con líneas faltantes
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML
pytest --cov=app --cov-report=html

# Generar ambos
pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Ver Reporte HTML

```bash
# Abrir en navegador
# En Linux:
xdg-open htmlcov/index.html

# En Mac:
open htmlcov/index.html

# En Windows:
start htmlcov/index.html
```

### Cobertura por Módulo

```bash
# Solo cobertura de autenticación
pytest --cov=app.auth test/unit/test_auth_unit.py

# Solo cobertura de routers
pytest --cov=app.routers test/integration/
```

### Verificar Cobertura Mínima

El proyecto requiere **80% de cobertura mínima** (configurado en `pytest.ini`).

```bash
# Falla si cobertura < 80%
pytest --cov=app --cov-fail-under=80
```

**Cobertura actual del proyecto: ~90%**

---

## 🧪 Tipos de Tests

### Tests Unitarios (`test/unit/`)

Tests que prueban funciones y métodos individuales sin dependencias externas.

**Características:**
- ✅ No requieren base de datos
- ✅ Ejecución muy rápida
- ✅ Prueban lógica de negocio aislada
- ✅ Marcados con `@pytest.mark.unit`

**Ejemplos:**
- Validación de hash de contraseñas
- Creación de tokens JWT
- Validación de modelos Pydantic
- Funciones de utilidad

**Ejemplo de test unitario:**

```python
import pytest
from app.auth import verify_password, get_password_hash

@pytest.mark.unit
def test_password_hash_verification():
    """Test que el hash de contraseña puede ser verificado"""
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)
```

### Tests de Integración (`test/integration/`)

Tests que prueban endpoints completos con todas sus dependencias.

**Características:**
- ✅ Usan base de datos SQLite en memoria
- ✅ Prueban flujos completos
- ✅ Verifican interacción entre componentes
- ✅ Marcados con `@pytest.mark.integration`

**Ejemplos:**
- Login y autenticación completa
- Creación y actualización de casos
- Gestión de usuarios con permisos
- Upload y descarga de archivos

**Ejemplo de test de integración:**

```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_case_success(
    client: AsyncClient,
    admin_headers: dict
):
    """Test de creación de caso exitosa"""
    case_data = {
        "title": "Test Case",
        "description": "Test Description",
        "priority": "alta",
        "status": "abierto",
        "case_type": "incidente"
    }
    
    response = await client.post(
        "/cases/",
        json=case_data,
        headers=admin_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == case_data["title"]
    assert "id" in data
```

---

## 🎯 Fixtures Disponibles

Las fixtures están definidas en `test/conftest.py` y están disponibles para todos los tests.

### Fixtures de Base de Datos

```python
@pytest.fixture
def db_session():
    """Sesión de base de datos para tests"""
    # Base de datos SQLite en memoria
    # Se limpia automáticamente después de cada test
```

```python
@pytest.fixture
def client():
    """Cliente HTTP de prueba (AsyncClient)"""
    # Cliente configurado para hacer requests a la API
```

### Fixtures de Usuarios

```python
@pytest.fixture
def admin_user():
    """Usuario con rol ADMIN"""
    # Usuario pre-creado para tests
```

```python
@pytest.fixture
def ingreso_user():
    """Usuario con rol INGRESO"""
```

```python
@pytest.fixture
def consulta_user():
    """Usuario con rol CONSULTA"""
```

### Fixtures de Autenticación

```python
@pytest.fixture
def admin_token():
    """Token JWT válido para admin"""
```

```python
@pytest.fixture
def admin_headers():
    """Headers HTTP con autenticación de admin"""
    # Incluye: {"Authorization": "Bearer <token>"}
```

### Fixtures de Casos

```python
@pytest.fixture
def sample_case():
    """Un caso de ejemplo"""
```

```python
@pytest.fixture
def multiple_cases():
    """Lista de 10 casos con diferentes estados"""
```

### Ejemplo de Uso

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_case_by_id(
    client: AsyncClient,
    admin_headers: dict,
    sample_case: Case
):
    response = await client.get(
        f"/cases/{sample_case.id}",
        headers=admin_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_case.id
```

---

## 🎨 Marcadores (Markers)

Los tests están organizados con marcadores para ejecución selectiva:

```python
@pytest.mark.unit          # Test unitario
@pytest.mark.integration   # Test de integración
@pytest.mark.auth          # Test de autenticación
@pytest.mark.cases         # Test de casos
@pytest.mark.users         # Test de usuarios
@pytest.mark.slow          # Test que toma tiempo
```

### Combinar Marcadores

```bash
# Tests unitarios de autenticación
pytest -m "unit and auth"

# Tests de integración de casos
pytest -m "integration and cases"

# Todos excepto los lentos
pytest -m "not slow"

# Unitarios o de autenticación
pytest -m "unit or auth"
```

---

## ✅ Buenas Prácticas

### 1. Nombres Descriptivos

```python
# ✅ BIEN
def test_admin_can_create_case_with_all_fields():
    ...

# ❌ MAL
def test_case_1():
    ...
```

### 2. Tests Independientes

```python
# ✅ BIEN - Cada test crea sus propios datos
@pytest.mark.integration
async def test_delete_case(client, admin_headers):
    # Crear caso para este test
    case = await create_test_case()
    
    # Eliminar
    response = await client.delete(f"/cases/{case.id}", headers=admin_headers)
    assert response.status_code == 200

# ❌ MAL - Depende de datos de otro test
@pytest.mark.integration
async def test_delete_case_2(client, admin_headers):
    # Asume que existe caso con id=1
    response = await client.delete("/cases/1", headers=admin_headers)
    ...
```

### 3. Usar Fixtures

```python
# ✅ BIEN - Usa fixture
@pytest.mark.integration
async def test_with_fixture(client, sample_case):
    response = await client.get(f"/cases/{sample_case.id}")
    ...

# ❌ MAL - Crea datos manualmente
@pytest.mark.integration
async def test_without_fixture(client):
    # Mucha configuración repetitiva...
    user = User(...)
    db.add(user)
    case = Case(...)
    db.add(case)
    ...
```

### 4. Tests Atómicos

```python
# ✅ BIEN - Un test, una verificación principal
def test_password_hash_is_valid():
    password = "test123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)

# ❌ MAL - Muchas verificaciones no relacionadas
def test_everything():
    # Test de hash
    ...
    # Test de JWT
    ...
    # Test de validación
    ...
```

### 5. Documentar Tests Complejos

```python
@pytest.mark.integration
async def test_complex_workflow(client, admin_headers):
    """
    Test del flujo completo de creación y actualización de caso.
    
    Flujo:
    1. Crear caso como admin
    2. Verificar que se creó correctamente
    3. Actualizar el caso
    4. Verificar actualización
    5. Verificar que el historial se guardó
    """
    # Implementación...
```

---

## 🔍 Debugging

### Usar Python Debugger (pdb)

```bash
# Detener en fallos
pytest --pdb

# Detener en el primer fallo
pytest -x --pdb
```

### Ver Traceback Completo

```bash
pytest --tb=long
```

### Ejecutar Solo Tests que Fallaron

```bash
# Último test fallido
pytest --lf

# Tests fallidos primero, luego el resto
pytest --ff
```

### Aumentar Verbosidad

```bash
# Ver cada test ejecutado
pytest -v

# Ver detalles de cada assert
pytest -vv
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"

**Solución:**

```bash
# Asegurarse de estar en el directorio correcto
cd backend

# Verificar que el entorno virtual está activo
source .venv/bin/activate

# Verificar que las dependencias están instaladas
pip list | grep fastapi
```

### Error: "Database is locked"

**Causa:** Los tests usan SQLite en memoria, esto no debería ocurrir.

**Solución:**
- Verificar que las fixtures usan `async with` correctamente
- Reiniciar pytest

### Tests Muy Lentos

**Solución:**

```bash
# Instalar pytest-xdist
pip install pytest-xdist

# Ejecutar en paralelo
pytest -n auto
```

### Error: "Event loop is closed"

**Causa:** Problema con pytest-asyncio

**Solución:**

```bash
# Verificar configuración en pytest.ini
asyncio_mode = auto

# O usar el marcador en cada test
@pytest.mark.asyncio
async def test_something():
    ...
```

---

## 📚 Recursos Adicionales

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [HTTPX Testing](https://www.python-httpx.org/advanced/#testing)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

## 🤝 Contribuir con Tests

Al agregar nuevas funcionalidades:

1. ✅ Escribir tests unitarios para lógica de negocio
2. ✅ Escribir tests de integración para endpoints
3. ✅ Mantener cobertura >80%
4. ✅ Ejecutar todos los tests antes de PR
5. ✅ Actualizar esta documentación si es necesario

---

## 📞 Contacto

Para dudas sobre testing:

- **Allan Córdova**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- **José Briones**: [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
- **Larry Sánchez**: [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
- **Ronny Ortiz**: [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

---

**Última actualización:** Enero 2026  
**Versión:** 2.0.0
