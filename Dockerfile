FROM python:3.11-slim

# Install system dependencies needed for network fetching, script execution, and parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gawk \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy full application code
COPY . .