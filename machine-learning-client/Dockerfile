# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc portaudio19-dev

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire machine-learning-client directory contents into the container at /app
COPY . /app

# Define the command to run your app
CMD ["python", "ml_service.py"]
