
FROM python:3.12-slim

# Install system dependencies needed for TA-lib and builds
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libta-lib0 \
    libta-lib0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install python dependencies (including ta-lib)
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.12-slim

# Install dependencies and TA-Lib library
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libta-lib0 \
    libta-lib0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Start the bot
CMD ["python", "bot.py"]
# Copy rest of app
COPY . .

# Run the 
    
