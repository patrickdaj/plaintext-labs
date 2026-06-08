FROM ubuntu:22.04
ARG TARGETARCH
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
# Install osquery (pinned release, cross-arch; TARGETARCH injected by BuildKit: amd64|arm64)
RUN curl -fsSL \
      "https://github.com/osquery/osquery/releases/download/5.12.1/osquery_5.12.1-1.linux_${TARGETARCH}.deb" \
      -o /tmp/osquery.deb && \
    dpkg -i /tmp/osquery.deb && rm /tmp/osquery.deb
WORKDIR /lab
COPY . /lab
