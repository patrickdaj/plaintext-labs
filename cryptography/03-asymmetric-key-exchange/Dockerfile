# Module 03 — Asymmetric & Key Exchange
# OpenSSL + Python cryptography
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl \
      time \
      less \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography==42.0.8

WORKDIR /lab
COPY . /lab

CMD ["bash"]
