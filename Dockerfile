# Build stage
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install build dependencies and python packages
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY src/ ./src/
COPY requirements.txt .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["python", "-m", "src.main"]
