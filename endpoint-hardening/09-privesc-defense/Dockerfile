# Module 09 — Local Privilege-Escalation Defense
# Ubuntu 22.04 with a deliberate SUID misconfiguration + AppArmor tools
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      apparmor \
      apparmor-utils \
      python3 \
      sudo \
      vim \
      less \
      findutils \
      procps \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Create a low-privileged user
RUN useradd -m -s /bin/bash appuser && \
    echo "appuser:appuser" | chpasswd

# Create the deliberate SUID misconfiguration:
# Copy 'find' to a custom location and set SUID bit
# (In a real environment, this would be vim, python, etc.)
RUN cp /usr/bin/find /usr/local/bin/find-suid && \
    chmod u+s /usr/local/bin/find-suid && \
    echo "Deliberate SUID binary created at /usr/local/bin/find-suid"

# Note: the GTFOBins technique for find with SUID:
# ./find-suid . -exec /bin/sh -p \; -quit
# This gives a root shell because find-suid runs as root (SUID)

WORKDIR /lab
COPY . /lab

CMD ["bash"]
