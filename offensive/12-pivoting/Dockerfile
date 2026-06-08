FROM python:3.12-slim
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        iproute2 curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /lab
COPY . /lab
