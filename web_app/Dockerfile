# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

RUN echo 'Acquire::http::Timeout "300";' > /etc/apt/apt.conf.d/99timeout

# Install system dependencies
RUN apt-get update && \
    apt-get install --fix-missing -y gcc portaudio19-dev ffmpeg

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the command to run your app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
