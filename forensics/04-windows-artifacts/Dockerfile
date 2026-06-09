FROM python:3.12-slim

# Install chainsaw (Rust binary) and python-registry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install chainsaw (latest release binary for Linux x86_64)
RUN CHAINSAW_VERSION=2.9.0 && \
    curl -fsSL "https://github.com/WithSecureLabs/chainsaw/releases/download/v${CHAINSAW_VERSION}/chainsaw_x86_64-unknown-linux-musl.tar.gz" \
    | tar -xz -C /usr/local/bin/ --strip-components=1 chainsaw/chainsaw && \
    chmod +x /usr/local/bin/chainsaw

# Install python-registry and python-evtx
RUN pip install --no-cache-dir python-registry==1.3.1

WORKDIR /lab
COPY . /lab/
