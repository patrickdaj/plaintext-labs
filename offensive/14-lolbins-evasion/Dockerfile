FROM debian:12-slim
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        python3 curl wget cron procps && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /lab
COPY . /lab
