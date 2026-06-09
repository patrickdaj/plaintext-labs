# Module 06 — Configuration Management
# Ansible controller targeting localhost (single-container demo)
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      openssh-client \
      openssh-server \
      sudo \
      auditd \
      libpam-pwquality \
      less \
      jq \
      curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ansible via pip (pinned version)
RUN pip3 install --no-cache-dir ansible==9.4.0

# Configure SSH for localhost targeting
RUN mkdir -p /run/sshd && \
    ssh-keygen -A && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

# Create an inventory file for localhost
RUN mkdir -p /lab
COPY . /lab
RUN echo "[target]\nlocalhost ansible_connection=local" > /lab/inventory

WORKDIR /lab
CMD ["bash"]
