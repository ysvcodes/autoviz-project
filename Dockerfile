# Dockerfile for autoviz-project
# Author: Atirola Adesanya
# File Purpose: Defines the Docker image for the autoviz-project.
# Base Image: Python 3.9-slim

FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies including pytest for testing
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and tests into the container
COPY ./app ./app

# Make port 5000 available (Flask app runs on this port by default)
EXPOSE 5000

# Command to run the application (for testing, Flask dev server is okay)
# For actual deployment stage in Jenkins, we might override or use Gunicorn
# For running tests with `docker run ... pytest`, this CMD isn't directly used for tests.
CMD ["python", "./app/main.py"] 
