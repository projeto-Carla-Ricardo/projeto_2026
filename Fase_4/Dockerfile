FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary

# Copiar código
COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /app/backend

# Variáveis de ambiente
ENV FLASK_APP=app
ENV FLASK_ENV=production

EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/ailo/camadas')" || exit 1

# Comando de arranque
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
