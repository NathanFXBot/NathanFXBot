FROM python:3.12-slim

# Install system dependencies needed for ta-lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libta-lib0 \
    libta-lib0-dev \
 && rm -rf /var/lib/apt/lists/*

# Install ta-lib source (sometimes needed)
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
 && tar -xzf ta-lib-0.4.0-src.tar.gz \
 && cd ta-lib && ./configure --prefix=/usr && make && make install \
 && cd .. && rm -rf ta-lib ta-lib-0.4.0-# Use an official Python slim image (Debian-based)
FROM python:3.12-slim

# Install build tools and wget to download TA-Lib source
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install TA-Lib C library from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run your bot when the container starts
CMD ["python", "bot.py"]
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
    
