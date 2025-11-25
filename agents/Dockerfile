# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY .env .env

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Install project dependencies
RUN uv pip install --system -e .

# Install visualization dependencies
RUN uv pip install --system matplotlib seaborn pandas numpy

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd -m -u 1000 pharma_user && \
    chown -R pharma_user:pharma_user /app

# Switch to non-root user
USER pharma_user

# Expose port if needed for future web interface
EXPOSE 8000

# Default command
CMD ["python", "-m", "pharma_researcher.main"]
