# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend Python files
COPY backend/*.py .

# Expose port (Render uses PORT env variable)
EXPOSE 10000

# Run with gunicorn - use PORT env variable if available
CMD gunicorn --bind 0.0.0.0:${PORT:-10000} --timeout 120 --workers 2 app:app
