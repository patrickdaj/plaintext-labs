FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir typer==0.15.2 httpx==0.28.1 rich==13.9.4

COPY . /lab

CMD ["sleep", "infinity"]
