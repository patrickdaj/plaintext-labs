# Module 02 — Symmetric & AEAD
# Python with cryptography library for GCM/ChaCha20 demos
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl \
      xxd \
      less \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir cryptography==42.0.8

WORKDIR /lab
COPY . /lab
COPY data/plaintext.txt /lab/data/plaintext.txt

CMD ["bash"]
