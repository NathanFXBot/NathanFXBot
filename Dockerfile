
FROM python:3.12

# Install system packages including TA-Lib dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libtool \
    libffi-dev \
    libta-lib0 \
    libta-lib0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your bot code
COPY . .

# Run your bot
CMD ["python", "bot.py"]
