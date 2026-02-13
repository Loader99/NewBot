# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y gcc python3-pip

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pyTelegramBotAPI

# Compile C file with pthread
RUN gcc -pthread direct_flood.c -o udp_flood

# Give execute permission
RUN chmod +x udp_flood

# Start the bot
CMD ["python", "bot.py"]