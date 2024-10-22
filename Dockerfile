# Use official Python image as base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies: wget, unzip, Chromium, Playwright dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    chromium-browser \
    chromium-chromedriver && \
    apt-get clean

# Download and install Ollama for Linux
RUN wget https://ollama.com/download/linux -O /tmp/ollama.zip && \
    unzip /tmp/ollama.zip -d /opt/ollama && \
    chmod +x /opt/ollama/ollama && \
    ln -s /opt/ollama/ollama /usr/local/bin/ollama

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN playwright install-deps && \
    playwright install

# Pull the necessary Ollama models
RUN ollama pull mistral && \
    ollama pull nomic-embed-text

# Copy the Python script and other files into the container
COPY . .

# Expose the port for Ollama API
EXPOSE 11434

# Start Ollama models in the background and run the app
CMD ollama run mistral & ollama run nomic-embed-text & python app.py
