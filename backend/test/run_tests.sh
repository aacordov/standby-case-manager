#!/bin/bash

# Script para ejecutar tests del proyecto Standby Case Manager
# Uso: ./run_tests.sh [opción]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Standby Case Manager - Tests${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Función para mostrar ayuda
show_help() {
    echo "Uso: ./run_tests.sh [opción]"
    echo ""
    echo "Opciones:"
    echo "  all          - Ejecutar todos los tests (por defecto)"
    echo "  unit         - Ejecutar solo tests unitarios"
    echo "  integration  - Ejecutar solo tests de integración"
    echo "  auth         - Ejecutar tests de autenticación"
    echo "  cases        - Ejecutar tests de casos"
    echo "  users        - Ejecutar tests de usuarios"
    echo "  coverage     - Ejecutar tests con reporte de cobertura HTML"
    echo "  quick        - Ejecutar tests sin cobertura (más rápido)"
    echo "  verbose      - Ejecutar tests en modo verbose"
    echo "  parallel     - Ejecutar tests en paralelo (requiere pytest-xdist)"
    echo "  help         - Mostrar esta ayuda"
    echo ""
}

# Función para ejecutar tests
run_tests() {
    local marker=$1
    local extra_args=$2
    
    if [ -z "$marker" ]; then
        echo -e "${GREEN}Ejecutando todos los tests...${NC}"
        pytest $extra_args
    else
        echo -e "${GREEN}Ejecutando tests: $marker${NC}"
        pytest -m "$marker" $extra_args
    fi
}

# Procesar argumentos
case "${1:-all}" in
    all)
        run_tests ""
        ;;
    unit)
        run_tests "unit"
        ;;
    integration)
        run_tests "integration"
        ;;
    auth)
        run_tests "auth"
        ;;
    cases)
        run_tests "cases"
        ;;
    users)
        run_tests "users"
        ;;
    coverage)
        echo -e "${GREEN}Ejecutando tests con reporte de cobertura HTML...${NC}"
        pytest --cov=app --cov-report=html --cov-report=term
        echo -e "${YELLOW}Reporte HTML generado en: htmlcov/index.html${NC}"
        ;;
    quick)
        echo -e "${GREEN}Ejecutando tests sin cobertura (modo rápido)...${NC}"
        pytest --no-cov
        ;;
    verbose)
        echo -e "${GREEN}Ejecutando tests en modo verbose...${NC}"
        pytest -v
        ;;
    parallel)
        echo -e "${GREEN}Ejecutando tests en paralelo...${NC}"
        pytest -n auto
        ;;
    help)
        show_help
        exit 0
        ;;
    *)
        echo -e "${YELLOW}Opción desconocida: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

# Mostrar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Tests completados exitosamente${NC}"
else
    echo ""
    echo -e "${YELLOW}✗ Algunos tests fallaron${NC}"
    exit 1
fi
