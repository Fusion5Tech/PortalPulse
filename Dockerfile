FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies required by some Python packages (e.g., psycopg2-binary fallback builds).
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Use uv for dependency resolution/install.
RUN pip install --no-cache-dir uv

# Copy dependency metadata first for better layer caching.
COPY pyproject.toml uv.lock ./

# Create project virtualenv and install dependencies from lockfile.
RUN uv sync --frozen

# Copy application source.
COPY . .

EXPOSE 8000

# Production entrypoint.
CMD [".venv/bin/gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "2"]
