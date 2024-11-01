# # Use Python 3.8 as the base image
# FROM python:3.8

# # Install OpenLDAP development libraries
# RUN apt-get update && apt-get install -y \
#     libsasl2-dev \
#     python3-dev \
#     libldap2-dev \
#     libssl-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Set the working directory within the container
# WORKDIR /app/backend

# # Copy the requirements.txt file to the container
# COPY requirements.txt .
# COPY static/ static/

# # Install Python dependencies using pip
# RUN python -m venv venv && \
#     . venv/bin/activate && \
#     pip install --no-cache-dir -r requirements.txt

# # Copy the entire application code to the container
# COPY . .

# # Expose port 8080 to the outside world
# EXPOSE 8080

# # Run the Django application
# CMD ["sh", "-c", ". venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
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

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment and install urllib3 version 1.25.11 first
RUN . venv/bin/activate && pip install urllib3==1.25.11

# Install the other dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Update urllib3 to version 2.2.3
RUN . venv/bin/activate && pip install --upgrade urllib3
# Copy the entire application code to the container
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Run the Django application
CMD ["sh", "-c", ". venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]