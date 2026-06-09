FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir httpx==0.28.1 beautifulsoup4==4.13.3

COPY . /lab

RUN mkdir -p /lab/output

CMD ["sleep", "infinity"]
