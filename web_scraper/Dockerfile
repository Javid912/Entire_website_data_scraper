# syntax=docker/dockerfile:1
FROM python:3.9-slim as base

# System dependencies for Scrapy, Playwright, Flask
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -ms /bin/bash appuser
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers as root (before switching user)
RUN pip install --no-cache-dir playwright && \
    python -m playwright install --with-deps chromium

# Copy the rest of the code
COPY . .

# Set permissions and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Default command (can be overridden by docker-compose)
CMD ["python", "flask_app/app.py"] 