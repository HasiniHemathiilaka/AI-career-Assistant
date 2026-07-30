# Use official lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies & Rust toolchain required for compiling binary wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    cargo \
    rustc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and wheel to ensure pre-compiled binary packages are pulled
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project code
COPY . .

# Expose Streamlit app port (8501) and Prometheus metrics port (8000)
EXPOSE 8501
EXPOSE 8000

# Start Streamlit application
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]