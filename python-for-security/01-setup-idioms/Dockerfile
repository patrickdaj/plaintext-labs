FROM python:3.12.9-slim

WORKDIR /lab

# Install ruff and bandit
RUN pip install --no-cache-dir ruff==0.9.10 bandit==1.8.3

COPY . /lab

CMD ["sleep", "infinity"]
