FROM python:3.12.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git && \
    curl -sSLo /usr/local/bin/gitleaks \
      https://github.com/gitleaks/gitleaks/releases/download/v8.24.0/gitleaks_8.24.0_linux_x64.tar.gz \
      | tar -xz -C /usr/local/bin/ gitleaks && \
    chmod +x /usr/local/bin/gitleaks && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /lab

COPY . /lab

CMD ["sleep", "infinity"]
