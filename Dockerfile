# Use the official Python image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the dependencies
RUN pip install -r requirements.txt

# Run the command to start uWSGI
CMD ["python", "app.py"]