# Production Dockerfile for Vedic Samhita Panchangam System
FROM python:3.11-slim

# Prevent Python from writing .pyc and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/Jyotisha:/app/panchangam_api"

WORKDIR /app

# Install system compilation packages for pyswisseph (Swiss Ephemeris C binding)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python production dependencies
COPY panchangam_api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Jyotisha core engine
COPY Jyotisha /app/Jyotisha

# Copy Panchangam API and frontend assets
COPY panchangam_api /app/panchangam_api

WORKDIR /app/panchangam_api

# Expose port 8000
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Launch Uvicorn with standard production settings
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
