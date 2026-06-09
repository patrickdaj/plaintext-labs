FROM python:3.12.9-slim

WORKDIR /lab

# Install checkov and tfsec
RUN pip install --no-cache-dir checkov==3.2.395

# tfsec via curl
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -sSLo /usr/local/bin/tfsec \
      https://github.com/aquasecurity/tfsec/releases/download/v1.28.11/tfsec-linux-amd64 && \
    chmod +x /usr/local/bin/tfsec && \
    rm -rf /var/lib/apt/lists/*

COPY . /lab

CMD ["sleep", "infinity"]
