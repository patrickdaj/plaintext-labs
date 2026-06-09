FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sleuthkit \
    python3 \
    python3-pip \
    e2fsprogs \
    dosfstools \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/ /scripts/
COPY data/ /data/

RUN chmod +x /scripts/*.sh /scripts/*.py 2>/dev/null || true

WORKDIR /lab
