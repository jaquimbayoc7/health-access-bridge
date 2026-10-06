FROM python:3.11-slim

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY icf ./icf

# Solo escucha en la interfaz local: el acceso externo pasa por Caddy (token) y Tailscale Funnel.
EXPOSE 8100
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8100"]
