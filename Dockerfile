# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /data

# Copy the current directory contents into the container at /app
COPY . /data

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run the application
CMD ["python", "main.py"]