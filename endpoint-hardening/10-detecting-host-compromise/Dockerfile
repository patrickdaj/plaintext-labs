# Module 10 — Detecting Host Compromise
# Python container with sigma-cli, PyYAML, and sample alert data
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      jq \
      less \
    && rm -rf /var/lib/apt/lists/*

# Install sigma-cli and dependencies
RUN pip install --no-cache-dir \
      sigma-cli==1.0.1 \
      pysigma-backend-splunk==1.0.3 \
      pysigma-backend-elasticsearch==1.1.2 \
      pyyaml==6.0.1

# Create rules directory
RUN mkdir -p /lab/rules

WORKDIR /lab
COPY . /lab

CMD ["bash"]
