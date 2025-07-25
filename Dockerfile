# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering and ensure UTF-8 encoding
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for LightFM and others
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    libsqlite3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY main.py .
COPY lightfm_model.pkl .
COPY .env .




# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
