FROM python:3.11-slim

# Install gcc
RUN sudo apt update && sudo apt install gcc python3-pip -y pip install pyTelegramBotAPI 

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Compile C file
RUN gcc direct_flood.c -o udp_flood

# Compile C file with pthread support
RUN gcc -pthread direct_flood.c -o udp_flood

# ✅ Give execute permission
RUN chmod +x udp_flood

# Start bot
CMD ["python", "bot.py"]