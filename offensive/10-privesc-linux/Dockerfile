FROM debian:12-slim

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        bash python3 sudo procps findutils cron vim-tiny && \
    rm -rf /var/lib/apt/lists/*

# Create a low-privilege user to simulate initial foothold
RUN useradd -m -u 1001 -s /bin/bash appuser && \
    echo "appuser:appuser" | chpasswd

# ── Planted misconfigurations ────────────────────────────────────────────────

# 1. SUID bit on find — lets any user run 'find' with euid=root
RUN chmod u+s /usr/bin/find

# 2. Permissive sudo rule — appuser can run find and vim as root, no password
RUN echo "Defaults !requiretty\nappuser ALL=(ALL) NOPASSWD: /usr/bin/find, /usr/bin/vim.tiny" \
    >> /etc/sudoers

# 3. World-writable cron script running as root
RUN printf '#!/bin/bash\n/bin/tar -czf /var/backups/app.tar.gz /var/log/ 2>/dev/null\n' \
    > /usr/local/bin/backup.sh && \
    chmod 777 /usr/local/bin/backup.sh && \
    echo "*/5 * * * * root /usr/local/bin/backup.sh" >> /etc/crontab

WORKDIR /lab
COPY . /lab
