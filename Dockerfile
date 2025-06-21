FROM python:3.9-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    libtool \
    libffi-dev \
    libta-lib0 \
    libta-lib0-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir ta-lib==0.4.24 && \
    pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /app

# Copy bot code
COPY . .

# Run the bot
CMD ["python", "bot.py"]
