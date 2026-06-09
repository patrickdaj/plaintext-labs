FROM python:3.12.9-slim

WORKDIR /lab

RUN pip install --no-cache-dir \
    sigma-cli==1.2.0 \
    pySigma-backend-splunk==1.3.4 \
    pySigma-pipeline-sysmon==1.4.0 \
    pytest==8.3.5 \
    pyyaml==6.0.2

COPY . /lab

CMD ["sleep", "infinity"]
