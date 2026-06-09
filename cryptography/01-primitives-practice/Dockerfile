# Module 01 — Primitives in Practice
# OpenSSL + Python cryptography library
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl \
      xxd \
      jq \
      less \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography==42.0.8

WORKDIR /lab
COPY . /lab

CMD ["bash"]
