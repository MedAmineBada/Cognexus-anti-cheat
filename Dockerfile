# =============================================================================
# Stage 1: Builder
# Install dependencies into an isolated prefix so only the final artifacts
# are carried into the runtime image.
# =============================================================================
FROM python:3.12-slim AS builder

# Keeps Python from buffering stdout/stderr and prevents .pyc files on disk
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install dependencies into a target directory to keep the layer clean
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install -r requirements.txt


# =============================================================================
# Stage 2: Runtime
# Minimal image — only production code and installed packages.
# =============================================================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

# Create a non-root user for least-privilege execution
RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup --no-create-home appuser

WORKDIR /app

# Pull in installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source (secrets / .env excluded via .dockerignore)
COPY api/       ./api/
COPY config/    ./config/
COPY main.py    ./main.py

# Lock down ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Gunicorn with uvicorn workers is the production-grade choice.
# Adjust --workers to match your CPU count (2 * cores + 1 is a common baseline).
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
