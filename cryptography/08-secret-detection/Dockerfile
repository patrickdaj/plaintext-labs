# Module 08 — Secret Detection & Leakage
# gitleaks + trufflehog + seed git repo with planted credentials
FROM python:3.12-slim

ARG GITLEAKS_VERSION=8.18.4
ARG TRUFFLEHOG_VERSION=3.79.0

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      git \
      jq \
      less \
    && rm -rf /var/lib/apt/lists/*

# Install gitleaks
RUN curl -sSfL \
      "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
      | tar -xz -C /usr/local/bin gitleaks

# Install trufflehog
RUN curl -sSfL \
      "https://github.com/trufflesecurity/trufflehog/releases/download/v${TRUFFLEHOG_VERSION}/trufflehog_${TRUFFLEHOG_VERSION}_linux_amd64.tar.gz" \
      | tar -xz -C /usr/local/bin trufflehog && \
    chmod +x /usr/local/bin/trufflehog

WORKDIR /lab
COPY . /lab

# Initialize the seed repo with planted credentials
RUN bash /lab/data/init-repo.sh

CMD ["bash"]
