FROM python:3.12.9-slim

WORKDIR /lab

# scapy needs libpcap and libnet
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap-dev \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir scapy==2.6.1

COPY . /lab

RUN mkdir -p /lab/output

CMD ["sleep", "infinity"]
