# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir requests qdrant-client flask

# Expose necessary ports
EXPOSE 5000 6333 11434

# Run the script when the container starts
CMD ["python", "Search.py"]