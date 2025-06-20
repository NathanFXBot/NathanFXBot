# Use official Python slim image
FROM python:3.12-slim

# Install dependencies for building TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Download, build, and install TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set environment variable for linker to find TA-Lib libraries
ENV LD_LIBRARY_PATH=/usr/local/lib

# Set working directory
WORKDIR /app

# Copy dependency file(s)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all app files
COPY . .

# Run your bot
CMD ["python", "bot.py"]
