FROM python:3.12.9-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.1.0
COPY app.py /app/
CMD ["python", "app.py"]
