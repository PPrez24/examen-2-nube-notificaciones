# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add build arguments for SNS credentials
ARG AWS_REGION
ARG SNS_TOPIC_ARN
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN


# Set environment variables inside the container
ENV AWS_REGION=$AWS_REGION
ENV SNS_TOPIC_ARN=$SNS_TOPIC_ARN
ENV AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY
ENV AWS_SESSION_TOKEN
# Expose the port
EXPOSE 5002

# Start the application
CMD ["python", "app.py"]
