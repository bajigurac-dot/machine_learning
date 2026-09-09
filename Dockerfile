FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Siapkan folder data untuk persistensi database SQLite
RUN mkdir -p /app/data

COPY . .

ENV PORT=7860
ENV DATABASE_PATH=/app/data/studio_ml.db
EXPOSE 7860

VOLUME ["/app/data"]

# Gunicorn dengan 2 worker & timeout 120 detik, sangat stabil untuk EC2 Free Tier (1GB RAM)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "--timeout", "120", "app:app"]
