# Use an official lightweight Python base image
FROM python:3.8-slim

# Copy files
COPY . /app/

# Set working directory
WORKDIR /app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Your application's default run command
CMD ["pytest"]
