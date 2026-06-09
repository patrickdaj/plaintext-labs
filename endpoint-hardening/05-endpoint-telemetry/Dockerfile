# Module 05 — Endpoint Telemetry & EDR
# Ubuntu 22.04 with osquery daemon
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG OSQUERY_VERSION=5.11.0

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      wget \
      gnupg \
      apt-transport-https \
      python3 \
      python3-pip \
      jq \
      less \
      procps \
      net-tools \
      cron \
    && rm -rf /var/lib/apt/lists/*

# Install osquery
RUN curl -sSL https://pkg.osquery.io/deb/pubkey.gpg | gpg --dearmor > /usr/share/keyrings/osquery-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/osquery-keyring.gpg] https://pkg.osquery.io/deb deb main" \
      > /etc/apt/sources.list.d/osquery.list && \
    apt-get update && \
    apt-get install -y osquery=${OSQUERY_VERSION} && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY . /lab

CMD ["bash"]
