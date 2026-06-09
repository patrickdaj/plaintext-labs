# Module 10 — Auditing Applied-Crypto Failures (testssl.sh scanner)
FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssl \
      curl \
      wget \
      bsdextrautils \
      procps \
      dnsutils \
      grep \
      less \
      jq \
      python3 \
      bash \
    && rm -rf /var/lib/apt/lists/*

# Install testssl.sh (pinned)
RUN wget -q https://github.com/drwetter/testssl.sh/archive/refs/tags/3.2.tar.gz \
      -O /tmp/testssl.tar.gz && \
    tar -xzf /tmp/testssl.tar.gz -C /opt && \
    mv /opt/testssl.sh-3.2 /opt/testssl && \
    ln -s /opt/testssl/testssl.sh /usr/local/bin/testssl.sh && \
    rm /tmp/testssl.tar.gz

WORKDIR /lab
COPY . /lab

CMD ["bash"]
