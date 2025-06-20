﻿# AI Text Toolkit

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-lightgrey)](https://fastapi.tiangolo.com/)

> A modular, high-performance NLP microservice built with FastAPI and Hugging Face Transformers.

---

## 🚀 Features

- **Simplify** complex sentences using `t5-small` (prefix: `simplify: {text}`)
- **Summarize** long documents with `facebook/bart-large-cnn`
- **Paraphrase** input text via `ramsrigouthamg/t5_paraphraser` (sampling-enabled)
- **Sentiment Analysis** using `distilbert-base-uncased-finetuned-sst-2-english`
- **Modular Routers**: each NLP function lives in its own FastAPI router
- **Validated I/O**: Pydantic schemas for request/response models
- **Auto Docs**: Interactive Swagger at `/docs` and ReDoc at `/redoc`

---

## 📦 Installation

1. **Clone the repo**:

   ```bash
   git clone https://github.com/omer-ulucan/ai-text-toolkit.git
   cd ai-text-toolkit
   ```

2. **Create & activate virtual environment** (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows PowerShell: .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Running Locally

Start the service with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access endpoints:

- Root: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🛠️ API Endpoints

| Method | Path          | Description                            |
| ------ | ------------- | -------------------------------------- |
| POST   | `/simplify`   | Simplify complex English text          |
| POST   | `/summarize`  | Summarize long passages                |
| POST   | `/paraphrase` | Rephrase input sentences               |
| POST   | `/sentiment`  | Sentiment analysis (POSITIVE/NEGATIVE) |

**Request & Response**

```json
// Request
{ "text": "Your input text here..." }

// Response
{ "result": "Processed text here..." }
```

---

## 🐳 Docker Setup

Three files: `Dockerfile`, `docker-compose.yml`, `boot/docker-run.sh`.

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Create virtual env and set PATH
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set workdir
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app ./app

# Copy and prepare startup script
COPY boot/docker-run.sh /boot/docker-run.sh
RUN sed -i 's/\r$//' /boot/docker-run.sh && chmod +x /boot/docker-run.sh

# Expose and run
EXPOSE 8000
ENTRYPOINT ["/boot/docker-run.sh"]
```

### docker-compose.yml

```yaml
services:
  ai-text-toolkit:
    build: .
    container_name: ai-text-toolkit
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
    volumes:
      - ./app:/code/app:ro
      - ./boot:/boot:ro
```

### boot/docker-run.sh

```sh
#!/usr/bin/env sh
set -e

# Activate virtual env
. /opt/venv/bin/activate

# Change to code directory
cd /code

# Read host/port from env
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Launch Gunicorn with Uvicorn workers
exec gunicorn \
  -k uvicorn.workers.UvicornWorker \
  -b "$RUN_HOST:$RUN_PORT" \
  app.main:app
```

**To build & run:**

```bash
# Using Docker Compose
docker compose up --build
```
