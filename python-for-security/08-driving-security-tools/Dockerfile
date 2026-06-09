FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir pymisp==2.4.196 httpx==0.28.1 requests==2.32.3

COPY . /lab

CMD ["sleep", "infinity"]
