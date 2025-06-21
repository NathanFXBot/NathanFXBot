FROM frolvlad/alpine-python-machinelearning

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your bot code
COPY . .

# Start the bot
CMD ["python", "bot.py"]
