# Module 06 — PKI & Certificate Management
# step-ca + step CLI
FROM debian:12-slim

ARG STEP_CA_VERSION=0.27.4
ARG STEP_CLI_VERSION=0.27.3

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      wget \
      openssl \
      jq \
      less \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install step CLI
RUN wget -q "https://github.com/smallstep/cli/releases/download/v${STEP_CLI_VERSION}/step_linux_${STEP_CLI_VERSION}_amd64.tar.gz" \
      -O /tmp/step.tar.gz && \
    tar -xzf /tmp/step.tar.gz -C /tmp && \
    mv /tmp/step_${STEP_CLI_VERSION}/bin/step /usr/local/bin/step && \
    rm -rf /tmp/step.tar.gz /tmp/step_${STEP_CLI_VERSION}

# Install step-ca
RUN wget -q "https://github.com/smallstep/certificates/releases/download/v${STEP_CA_VERSION}/step-ca_linux_${STEP_CA_VERSION}_amd64.tar.gz" \
      -O /tmp/step-ca.tar.gz && \
    tar -xzf /tmp/step-ca.tar.gz -C /tmp && \
    mv /tmp/step-ca_${STEP_CA_VERSION}/bin/step-ca /usr/local/bin/step-ca && \
    rm -rf /tmp/step-ca.tar.gz /tmp/step-ca_${STEP_CA_VERSION}

# Create step user
RUN useradd -m -s /bin/bash step

WORKDIR /lab
COPY . /lab

CMD ["bash"]
