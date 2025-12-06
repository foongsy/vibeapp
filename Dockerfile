FROM python:3.13-bookworm

# Install system tools
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install Bun (JavaScript runtime & package manager)
# Setting BUN_INSTALL to /usr/local to make it available globally
ENV BUN_INSTALL="/usr/local"
RUN curl -fsSL https://bun.sh/install | bash

# Verify installations
RUN uv --version && bun --version
