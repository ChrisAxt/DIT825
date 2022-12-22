#Base image
FROM python:3.9

# Environment variable for the virtual environment path 
ENV VIRTUAL_ENV=/opt/venv

# Create virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Adds the virtualenv’s bin/ directory to the PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set python to run in unbuffered mode 
# (Stops python from buffering outputs)
ENV PYTHONUNBUFFERED 1

# Working directory 
WORKDIR /app

# Add all files into working directory 
ADD . /app

# Copy the requirements file into the working directory
COPY ./requirements.txt /app/requirements.txt

# Install packages listed in the requirements file
RUN pip install -r requirements.txt

<<<<<<< HEAD
# COPY ./application_default_credentials.json /app/application_default_credentials.json

# RUN curl -sSL https://sdk.cloud.google.com | bash

# ENV PATH $PATH:/root/google-cloud-sdk/bin

## Log in to google-cloud and set project
# RUN gcloud auth login --cred-file=/app/application_default_credentials.json && \
#    gcloud config set project 'dit825'

# Run tests for the app
RUN python manage.py test app
=======
# Run unittests
RUN python /app/testing/unit_tests.py
>>>>>>> ad239ba (Add dockerfile uploading model to google cloud)

# Run pytools file
RUN python -u /app/pytools.py

# Copy orking directory
COPY . /app

