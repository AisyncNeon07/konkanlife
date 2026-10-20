# ==============================================================================
# Multi-stage Production Dockerfile for Konkan Guide Django Application
# Python 3.11 Slim Bookworm + Non-Root User + Gunicorn + WhiteNoise/Nginx
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Dependencies in Isolated Virtualenv
# ------------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies for C-extensions (psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


# ------------------------------------------------------------------------------
# Stage 2: Minimal Production Runtime Container
# ------------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Install runtime libraries required by psycopg2, Pillow, and healthcheck probes
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged system user and group (non-root)
RUN groupadd -r -g 1000 django \
    && useradd -r -u 1000 -g django -d /app -s /bin/sh django

WORKDIR /app

# Copy built virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Prepare static and media mount points with proper permissions
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

# Copy application source code
COPY --chown=django:django . /app/

# Ensure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Run as non-root user
USER django

# Expose internal Gunicorn application port
EXPOSE 8000

# Container Health Check against lightweight /healthz/ endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/healthz/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]
