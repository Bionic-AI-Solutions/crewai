# Lightweight monitoring service
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy monitoring requirements
COPY requirements-monitor.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-monitor.txt

# Copy monitoring code
COPY monitoring/ ./monitoring/

# Create necessary directories
RUN mkdir -p /app/logs /app/metrics

# Set permissions
RUN chmod -R 755 /app && \
    chmod -R 777 /app/logs /app/metrics

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port for monitoring API
EXPOSE 8000

# Default command
CMD ["python", "-m", "monitoring.monitor"]

# Labels
LABEL maintainer="curriculum-development-team" \
      version="1.0.0" \
      description="Monitoring service for deep research"
