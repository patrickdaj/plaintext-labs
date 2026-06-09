FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir pytest==8.3.5 ruff==0.9.10 bandit==1.8.3 httpx==0.28.1

COPY . /lab

RUN mkdir -p /lab/tests

CMD ["sleep", "infinity"]
