FROM python:3.11-slim

WORKDIR /app

# Install minimal system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PORT=8000

CMD ["sh", "-c", "cd backend && python -m uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
