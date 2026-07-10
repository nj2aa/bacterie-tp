FROM python:3.12-slim
WORKDIR /app
COPY proto/ /app/proto/
COPY atrophie/server.py .
RUN pip install grpcio grpcio-tools prometheus-client
CMD ["python", "server.py"]
