# Build dependency wheels separately so build artifacts do not enter the runtime image.
FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.txt ./
RUN python -m pip wheel --wheel-dir /wheels -r requirements.txt


FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /wheels /wheels
COPY requirements.txt ./
RUN python -m pip install --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

COPY --chown=app:app app ./app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
