FROM python:3.7-slim

WORKDIR /app

# Install build tools (for xgboost)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first (for cache efficiency)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy remaining source code
COPY . .

EXPOSE 5000

CMD ["python", "-m", "src.server"]