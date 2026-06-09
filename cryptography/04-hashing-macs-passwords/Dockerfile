# Module 04 — Hashing, MACs & Passwords
# Python with argon2-cffi + cryptography; OpenSSL for HMAC
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl \
      less \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      argon2-cffi==23.1.0 \
      cryptography==42.0.8

WORKDIR /lab
COPY . /lab

CMD ["bash"]
