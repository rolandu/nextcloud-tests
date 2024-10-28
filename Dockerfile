# Use an official lightweight Python base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy only requirements.txt initially to leverage caching
COPY requirements.txt /app/

# Install requirements
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc libc-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . /app/

# Your application's default run command
CMD ["pytest"]
