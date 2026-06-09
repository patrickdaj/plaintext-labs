FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir httpx==0.28.1 tenacity==9.0.0 python-dotenv==1.0.1

COPY . /lab

RUN mkdir -p /lab/output

CMD ["sleep", "infinity"]
