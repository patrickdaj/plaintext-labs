FROM debian:bookworm-slim

# Install dc3dd and supporting tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    dc3dd \
    coreutils \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY . /lab/
