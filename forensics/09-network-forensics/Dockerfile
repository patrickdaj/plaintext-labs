FROM zeek/zeek:6.2.1-ubuntu

RUN apt-get update && apt-get install -y \
    tshark \
    python3 \
    python3-pip \
    scapy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /lab
COPY scripts/ /scripts/
COPY data/ /data/

RUN chmod +x /scripts/*.sh
