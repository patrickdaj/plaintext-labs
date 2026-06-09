FROM python:3.12.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    sshpass \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir ansible==11.4.0 ansible-lint==25.1.3

WORKDIR /ansible

COPY . /ansible

CMD ["sleep", "infinity"]
