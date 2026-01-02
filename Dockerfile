FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build dependencies (may be needed for some packages in requirements.txt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
# NOTE: `pip install -r requirements.txt` can be large and take a long time
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

# Use PORT env var when available, otherwise default to 8501
CMD streamlit run music.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true
