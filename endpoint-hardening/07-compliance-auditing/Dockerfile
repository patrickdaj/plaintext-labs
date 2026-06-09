# Module 07 — Compliance Scoring & Auditing
# Deliberately un-hardened Ubuntu 22.04 with Lynis + OpenSCAP
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG LYNIS_VERSION=3.1.1

RUN apt-get update && apt-get install -y --no-install-recommends \
      openscap-scanner \
      openscap-utils \
      ssg-base \
      ssg-debderived \
      wget \
      curl \
      python3 \
      python3-pip \
      procps \
      net-tools \
      less \
      jq \
      libpam-pwquality \
    && rm -rf /var/lib/apt/lists/*

# Install Lynis
RUN wget -q "https://github.com/CISOfy/lynis/archive/refs/tags/${LYNIS_VERSION}.tar.gz" \
      -O /tmp/lynis.tar.gz \
    && tar -xzf /tmp/lynis.tar.gz -C /opt \
    && mv /opt/lynis-${LYNIS_VERSION} /opt/lynis \
    && ln -s /opt/lynis/lynis /usr/local/bin/lynis \
    && rm /tmp/lynis.tar.gz

# Deliberately leave the host un-hardened (this is the "before" state)
# Default Ubuntu settings, no CIS controls applied

WORKDIR /lab
COPY . /lab

CMD ["bash"]
