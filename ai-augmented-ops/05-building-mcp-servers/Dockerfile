FROM python:3.12-slim
WORKDIR /lab
COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DATA_DIR=/lab/data
CMD ["python3", "server/server.py"]
