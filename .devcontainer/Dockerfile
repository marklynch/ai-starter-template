# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set environment variables optimised for container build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME --shell /bin/bash \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up locale (simple approach using C.UTF-8)
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
ENV LC_ALL=C.UTF-8

# Set work directory
WORKDIR /workspace

# Install basic Python tools (requirements will be installed post-create)
RUN pip install --upgrade pip setuptools wheel

# Create common directories as root first
RUN mkdir -p /workspace/tests \
    && mkdir -p /workspace/notebooks \
    && mkdir -p /workspace/data \
    && chown -R $USER_UID:$USER_GID /workspace

# Switch to non-root user
USER $USERNAME

# Create user-specific directories
RUN mkdir -p /home/$USERNAME/.cache/pip