#!/bin/bash

echo "=========================================="
echo "TESTS FRONTEND - Standby Case Manager"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: Debes ejecutar este script desde el directorio frontend${NC}"
    echo "Usa: cd frontend && ./run_tests.sh"
    exit 1
fi

# Verificar que node_modules existe
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules no encontrado. Instalando dependencias...${NC}"
    npm install
fi

# Función para ejecutar todos los tests
run_all_tests() {
    echo -e "${BLUE}🧪 Ejecutando TODOS los tests...${NC}"
    echo ""
    npm run test:run
    TEST_RESULT=$?
    echo ""
    if [ $TEST_RESULT -eq 0 ]; then
        echo -e "${GREEN}✅ Todos los tests pasaron!${NC}"
    else
        echo -e "${RED}❌ Algunos tests fallaron${NC}"
    fi
    return $TEST_RESULT
}

# Función para ejecutar tests en modo watch
run_watch() {
    echo -e "${BLUE}👀 Ejecutando tests en modo watch...${NC}"
    echo -e "${YELLOW}Los tests se ejecutarán automáticamente al cambiar archivos${NC}"
    echo -e "${YELLOW}Presiona 'q' para salir${NC}"
    echo ""
    npm run test:watch
}

# Función para ejecutar tests con UI
run_ui() {
    echo -e "${BLUE}🎨 Abriendo interfaz visual de tests...${NC}"
    echo ""
    npm run test:ui
}

# Función para ejecutar tests con cobertura
run_coverage() {
    echo -e "${BLUE}📊 Ejecutando tests con reporte de cobertura...${NC}"
    echo ""
    npm run test:coverage
    echo ""
    echo -e "${GREEN}✅ Reporte de cobertura generado${NC}"
    echo -e "${YELLOW}💡 Puedes ver el reporte HTML en: coverage/index.html${NC}"
    
    # Intentar abrir el reporte
    if command -v xdg-open &> /dev/null; then
        echo -e "${BLUE}Abriendo reporte en el navegador...${NC}"
        xdg-open coverage/index.html
    elif command -v open &> /dev/null; then
        echo -e "${BLUE}Abriendo reporte en el navegador...${NC}"
        open coverage/index.html
    fi
}

# Función para ejecutar tests de un archivo específico
run_specific() {
    echo -e "${BLUE}🎯 Ejecutando tests específicos: $1${NC}"
    echo ""
    npm run test:run -- "$1"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 {all|watch|ui|coverage|specific <file>|help}"
    echo ""
    echo "Comandos disponibles:"
    echo "  all         - Ejecutar todos los tests una vez"
    echo "  watch       - Ejecutar tests en modo watch (re-ejecuta al cambiar archivos)"
    echo "  ui          - Abrir interfaz visual de Vitest"
    echo "  coverage    - Ejecutar tests con reporte de cobertura"
    echo "  specific    - Ejecutar tests de un archivo específico"
    echo "  help        - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_tests.sh all"
    echo "  ./run_tests.sh watch"
    echo "  ./run_tests.sh coverage"
    echo "  ./run_tests.sh specific src/pages/__tests__/Login.test.tsx"
}

# Menú principal
case "$1" in
    all)
        run_all_tests
        ;;
    watch)
        run_watch
        ;;
    ui)
        run_ui
        ;;
    coverage)
        run_coverage
        ;;
    specific)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: Debes especificar un archivo${NC}"
            echo "Ejemplo: ./run_tests.sh specific src/pages/__tests__/Login.test.tsx"
            exit 1
        fi
        run_specific "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            # Si no hay argumentos, ejecutar todos los tests por defecto
            run_all_tests
        else
            echo -e "${RED}❌ Comando desconocido: $1${NC}"
            echo ""
            show_help
            exit 1
        fi
        ;;
esac
