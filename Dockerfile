# Base image
FROM python:3.10-slim-buster

# Install system dependencies
RUN apt update && apt install -y libpq-dev curl

# Set working directory
WORKDIR /app

# script to wait for PostgreSQL to become available
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "cows.main:app", "--host", "0.0.0.0", "--port", "8000"]
