# Production Dockerfile for Vedic Samhita Panchangam System
FROM python:3.11-slim

# Prevent Python from writing .pyc and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/panchangam_api:/app/Jyotisha"

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

# Expose port (supports Render $PORT or default 8000)
EXPOSE 8000
EXPOSE 10000

# Launch Uvicorn supporting dynamic PORT from cloud provider
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
