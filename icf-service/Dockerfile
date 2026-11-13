FROM python:3.11-slim

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY icf ./icf
# HU-07j: el servicio crea las tablas de la memoria de casos desde sql/002_cases.sql
COPY sql/002_cases.sql ./sql/002_cases.sql

# Solo escucha en la interfaz local: el acceso externo pasa por Caddy (token) y Tailscale Funnel.
EXPOSE 8100
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8100"]
