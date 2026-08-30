FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system django && adduser --system --ingroup django django
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app
COPY frontend/public/media /app/media
RUN chmod +x /app/entrypoint.sh && chown -R django:django /app

USER django
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
