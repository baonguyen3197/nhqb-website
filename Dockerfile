# Use Python 3.8 as the base image
FROM python:3.8-slim as base

# Install OpenLDAP development libraries and other dependencies
RUN apt-get update && apt-get install -y \
    libsasl2-dev \
    python3-dev \
    libldap2-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory within the container
WORKDIR /app/backend

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies using pip
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Use ENTRYPOINT to ensure the virtual environment is activated
ENTRYPOINT ["/bin/sh", "-c", ". venv/bin/activate && exec \"$0\" \"$@\"", "--"]

# Default command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]