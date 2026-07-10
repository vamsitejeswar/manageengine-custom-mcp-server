FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV HOST=0.0.0.0
ENV PORT=8080
ENV LOG_LEVEL=INFO

EXPOSE 8080

CMD ["python", "-m", "src.server"]
