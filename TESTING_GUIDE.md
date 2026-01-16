# 🧪 Guía Completa de Testing - Standby Case Manager

Esta guía proporciona instrucciones paso a paso para ejecutar tests en backend y frontend.

---

## 📋 Tabla de Contenidos

- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Testing con Docker](#testing-con-docker)
- [CI/CD Testing](#cicd-testing)
- [Solución de Problemas](#solución-de-problemas)

---

## 🐍 Backend Testing

### Requisitos Previos

- Python 3.11+
- pip o uv (gestor de paquetes)

### Paso 1: Crear Entorno Virtual

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows PowerShell:
.venv\Scripts\Activate.ps1

# En Windows CMD:
.venv\Scripts\activate.bat
```

### Paso 2: Instalar Dependencias

```bash
# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias de testing
pip install -r requirements-test.txt

# Verificar instalación
pip list
```

**Si `requirements-test.txt` no existe, crearlo con:**

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
```

### Paso 3: Ejecutar Tests

```bash
# Ejecutar TODOS los tests
pytest

# Solo tests unitarios
pytest test/unit -v

# Solo tests de integración
pytest test/integration -v

# Con reporte de cobertura
pytest --cov=app --cov-report=html

# En paralelo (más rápido)
pytest -n auto
```

### Paso 4: Ver Reporte de Cobertura

```bash
# Generar reporte HTML
pytest --cov=app --cov-report=html

# Abrir en navegador
# Linux:
xdg-open htmlcov/index.html

# Mac:
open htmlcov/index.html

# Windows:
start htmlcov/index.html
```

### Paso 5: Tests Específicos

```bash
# Por archivo
pytest test/unit/test_auth_unit.py -v

# Por clase
pytest test/unit/test_auth_unit.py::TestPasswordHashing -v

# Por función
pytest test/unit/test_auth_unit.py::TestPasswordHashing::test_password_hash -v

# Por nombre (keyword)
pytest -k "login" -v

# Por marca
pytest -m "unit" -v
pytest -m "integration" -v
pytest -m "auth" -v
```

### Estructura de Tests Backend

```
backend/
├── test/
│   ├── conftest.py              # Fixtures compartidas
│   ├── unit/                    # Tests unitarios (sin DB)
│   │   ├── test_auth_unit.py    # Tests de autenticación
│   │   └── test_models.py       # Tests de modelos
│   └── integration/             # Tests de integración (con DB)
│       ├── test_auth_integration.py
│       ├── test_cases_integration.py
│       └── test_users_integration.py
└── pytest.ini                   # Configuración pytest
```

### Tipos de Tests Backend

| Tipo | Ubicación | Descripción | Velocidad |
|:-----|:----------|:------------|:----------|
| **Unitarios** | `test/unit/` | Lógica de negocio aislada | ⚡ Muy rápido |
| **Integración** | `test/integration/` | Endpoints completos con DB | 🐢 Más lento |

---

## ⚛️ Frontend Testing

### Requisitos Previos

- Node.js 18+ (se recomienda usar nvm)
- npm o bun

### Paso 1: Instalar Node.js con nvm

```bash
# Instalar nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Recargar shell
source ~/.bashrc
# O en Mac:
source ~/.zshrc

# Instalar Node.js LTS
nvm install --lts
nvm use --lts

# Verificar instalación
node --version
npm --version
```

### Paso 2: Instalar Dependencias del Proyecto

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias del proyecto
npm install

# Instalar dependencias de testing
npm install -D vitest @vitest/ui @vitest/coverage-v8 \
  @testing-library/react @testing-library/jest-dom \
  @testing-library/user-event jsdom msw
```

### Paso 3: Configurar Scripts de Testing

Verificar que `package.json` tiene estos scripts:

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

### Paso 4: Ejecutar Tests

```bash
# Modo interactivo (watch mode)
npm run test

# Una sola vez
npm run test:run

# Con UI visual
npm run test:ui

# Con cobertura
npm run test:coverage

# Usando el script bash (recomendado)
chmod +x run_tests.sh
./run_tests.sh
```

### Paso 5: Ver Reporte de Cobertura

```bash
# Generar reporte
npm run test:coverage

# Abrir reporte HTML
# Linux:
xdg-open coverage/index.html

# Mac:
open coverage/index.html

# Windows:
start coverage/index.html
```

### Script run_tests.sh

Crear `frontend/run_tests.sh` si no existe:

```bash
#!/bin/bash

# Script para ejecutar tests del frontend
# Autor: Equipo Standby Case Manager

echo "🧪 Iniciando tests del frontend..."
echo ""

# Verificar que node_modules existe
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules no encontrado. Ejecutando npm install..."
    npm install
fi

# Ejecutar tests con coverage
echo "📊 Ejecutando tests con cobertura..."
npm run test:coverage

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Tests completados exitosamente"
    echo "📁 Reporte de cobertura en: coverage/index.html"
else
    echo ""
    echo "❌ Algunos tests fallaron"
    exit 1
fi
```

### Estructura de Tests Frontend

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/
│   │       └── Button.test.tsx      # Test de componente
│   ├── pages/
│   │   └── __tests__/
│   │       ├── Login.test.tsx       # Test de página
│   │       └── Dashboard.test.tsx
│   ├── utils/
│   │   └── __tests__/
│   │       └── cn.test.ts           # Test de utilidad
│   └── test/
│       ├── setup.ts                 # Configuración global
│       ├── test-utils.tsx           # Utilidades de testing
│       └── mocks/
│           ├── handlers.ts          # MSW handlers
│           └── server.ts            # MSW server
├── vitest.config.ts                 # Configuración Vitest
└── run_tests.sh                     # Script de ejecución
```

### Tipos de Tests Frontend

| Tipo | Descripción | Herramienta |
|:-----|:------------|:------------|
| **Componentes** | Tests de componentes React aislados | React Testing Library |
| **Integración** | Tests de flujos de usuario completos | React Testing Library + MSW |
| **Utilidades** | Tests de funciones helper | Vitest |

---

## 🐳 Testing con Docker

### Opción 1: Tests en Contenedor Dedicado

```bash
# Backend
docker compose run --rm backend pytest

# Frontend
docker compose run --rm frontend npm run test:run
```

### Opción 2: Tests en Contenedor Existente

```bash
# Backend
docker compose exec backend pytest

# Frontend
docker compose exec frontend npm run test:run
```

### Crear Servicio de Testing en Docker Compose

Agregar a `docker-compose.yml`:

```yaml
services:
  backend-test:
    build: ./backend
    command: pytest --cov=app --cov-report=html
    volumes:
      - ./backend:/app
    environment:
      - TESTING=1
    depends_on:
      - db

  frontend-test:
    build: ./frontend
    command: npm run test:coverage
    volumes:
      - ./frontend:/app
    environment:
      - NODE_ENV=test
```

Ejecutar:

```bash
docker compose up backend-test
docker compose up frontend-test
```

---

## 🔄 CI/CD Testing

### GitHub Actions

Crear `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run tests
      run: |
        cd frontend
        npm run test:coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### GitLab CI

Crear `.gitlab-ci.yml`:

```yaml
stages:
  - test

backend-tests:
  stage: test
  image: python:3.11
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_pass
  script:
    - cd backend
    - pip install -r requirements.txt -r requirements-test.txt
    - pytest --cov=app --cov-report=term

frontend-tests:
  stage: test
  image: node:18
  script:
    - cd frontend
    - npm ci
    - npm run test:coverage
```

---

## 🛠️ Solución de Problemas

### Backend

#### Problema: "ModuleNotFoundError: No module named 'app'"

```bash
# Solución 1: Verificar directorio
cd backend
pwd  # Debe mostrar .../standby-case-manager/backend

# Solución 2: Verificar entorno virtual
source .venv/bin/activate
which python  # Debe mostrar .venv/bin/python

# Solución 3: Reinstalar dependencias
pip install -r requirements.txt -r requirements-test.txt
```

#### Problema: "Database is locked"

```bash
# Solución: Los tests usan SQLite en memoria, reiniciar pytest
pytest --cache-clear
```

#### Problema: Tests muy lentos

```bash
# Solución: Ejecutar en paralelo
pip install pytest-xdist
pytest -n auto
```

### Frontend

#### Problema: "Cannot find module 'vitest'"

```bash
# Solución: Instalar dependencias de testing
npm install -D vitest @vitest/ui @vitest/coverage-v8
```

#### Problema: "ReferenceError: document is not defined"

```bash
# Solución: Verificar que jsdom está configurado
# En vitest.config.ts:
export default defineConfig({
  test: {
    environment: 'jsdom',
  }
})
```

#### Problema: "./run_tests.sh: Permission denied"

```bash
# Solución: Dar permisos de ejecución
chmod +x run_tests.sh
```

---

## 📊 Metas de Cobertura

### Backend
- ✅ **Mínimo requerido**: 80%
- 🎯 **Meta actual**: 90%+
- 🔥 **Ideal**: 95%+

### Frontend
- ✅ **Mínimo requerido**: 70%
- 🎯 **Meta actual**: 80%+
- 🔥 **Ideal**: 90%+

---

## 📝 Checklist Antes de Commit

```bash
# Backend
cd backend
source .venv/bin/activate
pytest --cov=app --cov-fail-under=80
black --check .
flake8 .

# Frontend
cd frontend
npm run test:coverage
npm run lint
npm run build
```

---

## 📞 Soporte

Si tienes problemas con los tests, contacta:

- **Allan Córdova**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- **José Briones**: [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
- **Larry Sánchez**: [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
- **Ronny Ortiz**: [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

---

**Última actualización:** Enero 2026  
**Versión:** 2.0.0
