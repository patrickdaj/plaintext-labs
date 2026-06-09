# Module 07 — Secrets Management
# Vault CLI + sops + age + Python hvac
FROM python:3.12-slim

ARG VAULT_VERSION=1.17.2
ARG SOPS_VERSION=3.9.0
ARG AGE_VERSION=1.2.0

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      wget \
      unzip \
      jq \
      less \
      git \
    && rm -rf /var/lib/apt/lists/*

# Install Vault CLI
RUN curl -sSfL \
      "https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip" \
      -o /tmp/vault.zip && \
    unzip /tmp/vault.zip -d /usr/local/bin && \
    rm /tmp/vault.zip

# Install sops
RUN curl -sSfL \
      "https://github.com/mozilla/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux.amd64" \
      -o /usr/local/bin/sops && \
    chmod +x /usr/local/bin/sops

# Install age
RUN curl -sSfL \
      "https://github.com/FiloSottile/age/releases/download/v${AGE_VERSION}/age-v${AGE_VERSION}-linux-amd64.tar.gz" \
      | tar -xz -C /tmp && \
    mv /tmp/age/age /usr/local/bin/age && \
    mv /tmp/age/age-keygen /usr/local/bin/age-keygen && \
    rm -rf /tmp/age

# Install Python Vault client
RUN pip install --no-cache-dir hvac==2.3.0

WORKDIR /lab
COPY . /lab

CMD ["bash"]
