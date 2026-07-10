FROM python:3.12-slim
WORKDIR /app
COPY proto/ /app/proto/
COPY web/app.py .
RUN pip install grpcio grpcio-tools flask
CMD ["python", "app.py"]
