# ==========================================
# Backend Dockerfile - DESARROLLO (DEFAULT)
# ==========================================

FROM python:3.11-slim

# Metadata
LABEL maintainer="Standby Case Manager Team"
LABEL version="2.3.0"
LABEL description="Backend FastAPI"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv para instalación ultrarrápida
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN uv pip install --system --no-cache -r requirements.txt

# Copiar código (se sobreescribe con volumen en dev)
COPY . .

# Crear directorio uploads
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Comando por defecto (puede ser sobreescrito en docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]