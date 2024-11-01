
# Base image
from python:3.11-slim

# Set the working directory
workdir /app

# Copy requirements file
copy requirements.txt .

# Install dependencies
run pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
copy . .

# Command to run the application
cmd ["python", "app.py"]
