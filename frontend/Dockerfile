# ==========================================
# Frontend Dockerfile - DESARROLLO (DEFAULT)
# ==========================================


# Build stage - preparar dependencias
FROM oven/bun:1-alpine AS dependencies

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json bun.lock* ./

# Instalar dependencias
RUN bun install --frozen-lockfile

# ==========================================
# Development stage - Vite dev server
# ==========================================
FROM oven/bun:1-alpine AS development

# Metadata
LABEL maintainer="Standby Case Manager Team"
LABEL version="2.3.0"
LABEL description="Frontend React + Vite"

WORKDIR /app

# Copiar dependencias instaladas
COPY --from=dependencies /app/node_modules ./node_modules

# Copiar código (se sobreescribe con volumen en dev)
COPY . .

# Exponer puerto
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Comando: Vite dev server
CMD ["bun", "run", "dev", "--host", "0.0.0.0", "--port", "3000"]