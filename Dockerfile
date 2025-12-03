# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (including Rust for pydantic-core)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all backend Python files
COPY backend/*.py .

# Expose port (Render uses PORT env variable)
EXPOSE 10000

# Run with gunicorn - use PORT env variable if available
CMD gunicorn --bind 0.0.0.0:${PORT:-10000} --timeout 120 --workers 2 app:app
