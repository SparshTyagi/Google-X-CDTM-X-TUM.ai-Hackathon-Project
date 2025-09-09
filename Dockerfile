# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Reduces image size
# --upgrade pip: Best practice
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container at /app
# This includes your agents/, api.py, orchestrator.py, etc.
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your app using uvicorn
# 0.0.0.0 is crucial to allow connections from outside the container.
# The port must match the EXPOSE instruction.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]