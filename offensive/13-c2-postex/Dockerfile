FROM python:3.12-slim
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
        procps cron && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask==3.0.3
WORKDIR /lab
COPY . /lab
