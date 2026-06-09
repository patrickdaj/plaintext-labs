FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sleuthkit \
    foremost \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY . /lab/
