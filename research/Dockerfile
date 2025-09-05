# Use Python 3.11 slim image for better performance
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-install-project

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Create necessary directories
RUN mkdir -p /app/research_output /app/cache /app/logs

# Set permissions
RUN chmod -R 755 /app && \
    chmod -R 777 /app/research_output /app/cache /app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.append('/app/src'); import open_deep_research; print('Service healthy')" || exit 1

# Default command
CMD ["uv", "run", "python", "-m", "open_deep_research.deep_researcher"]

# Expose port for LangGraph Studio (if needed)
EXPOSE 2024

# Labels for better container management
LABEL maintainer="curriculum-development-team" \
      version="1.0.0" \
      description="Open Deep Research service for curriculum development"
