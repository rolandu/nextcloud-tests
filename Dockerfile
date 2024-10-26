# Use an official lightweight Python base image
FROM python:3.8-slim

# Copy files
COPY . /app/

# Set working directory
WORKDIR /app

# Install requirements
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Your application's default run command
CMD ["pytest"]
