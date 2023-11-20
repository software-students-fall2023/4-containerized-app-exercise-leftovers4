# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of application's code into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 5001

# Run application
CMD ["python", "ml_service.py"]
