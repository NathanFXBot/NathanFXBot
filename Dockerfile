FROM python:3.12-slim

# Install build dependencies for TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and build TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

# Set working directory
WORKDIR /app

# Copy your app
COPY . .

# Install Python dependencies (including ta-lib python binding)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
