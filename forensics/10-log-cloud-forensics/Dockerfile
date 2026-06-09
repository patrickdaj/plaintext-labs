FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Hayabusa (pre-built binary)
ARG HAYABUSA_VERSION=2.16.0
RUN curl -fsSL \
    "https://github.com/Yamato-Security/hayabusa/releases/download/v${HAYABUSA_VERSION}/hayabusa-${HAYABUSA_VERSION}-lin-x64-musl.zip" \
    -o /tmp/hayabusa.zip \
    && unzip /tmp/hayabusa.zip -d /tmp/hayabusa-extract \
    && find /tmp/hayabusa-extract -name "hayabusa*" -type f -exec cp {} /usr/local/bin/hayabusa \; \
    && chmod +x /usr/local/bin/hayabusa \
    && rm -rf /tmp/hayabusa.zip /tmp/hayabusa-extract

# Install Chainsaw (pre-built binary)
ARG CHAINSAW_VERSION=2.9.0
RUN curl -fsSL \
    "https://github.com/WithSecureLabs/chainsaw/releases/download/v${CHAINSAW_VERSION}/chainsaw_x86_64-unknown-linux-gnu.tar.gz" \
    -o /tmp/chainsaw.tar.gz \
    && tar -xzf /tmp/chainsaw.tar.gz -C /tmp \
    && cp /tmp/chainsaw/chainsaw /usr/local/bin/chainsaw \
    && chmod +x /usr/local/bin/chainsaw \
    && rm -rf /tmp/chainsaw.tar.gz /tmp/chainsaw

COPY scripts/ /scripts/
COPY data/ /data/

WORKDIR /lab
