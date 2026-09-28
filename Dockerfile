FROM python:3.11-slim

WORKDIR /app

# commit-oracle has zero third-party dependencies (pure standard library)
COPY . /app

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python3", "src/server.py"]
