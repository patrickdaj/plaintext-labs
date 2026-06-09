FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install plaso (log2timeline)
RUN pip install --no-cache-dir plaso==20231112

WORKDIR /lab
COPY . /lab/
