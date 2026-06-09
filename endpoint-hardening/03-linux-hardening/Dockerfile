# Module 03 — Linux Hardening to CIS
# Lynis + OpenSCAP + SCAP Security Guide (SSG) on Ubuntu 22.04
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
    && rm -rf /var/lib/apt/lists/*

# Install Lynis from the CISOfy repository for the pinned version
RUN wget -q "https://github.com/CISOfy/lynis/archive/refs/tags/${LYNIS_VERSION}.tar.gz" \
      -O /tmp/lynis.tar.gz \
    && tar -xzf /tmp/lynis.tar.gz -C /opt \
    && mv /opt/lynis-${LYNIS_VERSION} /opt/lynis \
    && ln -s /opt/lynis/lynis /usr/local/bin/lynis \
    && rm /tmp/lynis.tar.gz

WORKDIR /lab
COPY . /lab

CMD ["bash"]
