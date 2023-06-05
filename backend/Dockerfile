FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libpq-dev gcc netcat && \
    pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .
RUN chmod +x run_app.sh
ENTRYPOINT ["/app/run_app.sh"]
