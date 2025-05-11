# Use the official Python image from Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /data

RUN apt-get update && apt-get install -y git && apt-get clean

RUN git clone https://github.com/PXLCoarl/redh .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "main.py"]