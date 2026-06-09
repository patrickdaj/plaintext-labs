FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Volatility3
RUN pip install --no-cache-dir volatility3==2.5.0

WORKDIR /lab
COPY . /lab/
