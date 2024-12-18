# Use Python 3.8 as the base image
FROM python:3.8

# Install OpenLDAP development libraries
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

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source venv/bin/activate && pip install urllib3==1.25.11 && pip install --no-cache-dir -r requirements.txt && pip install --upgrade urllib3"

# Copy the entire application code to the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the Django application
CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8080"]