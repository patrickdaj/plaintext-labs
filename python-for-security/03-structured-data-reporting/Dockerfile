FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir rich==13.9.4

COPY . /lab

RUN mkdir -p /lab/output

CMD ["sleep", "infinity"]
