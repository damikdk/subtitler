# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Install uv for faster dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy dependency files (include README needed by build backend)
COPY pyproject.toml uv.lock README.md ./

# Install only production dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
