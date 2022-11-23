#Base image
FROM python:3

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

# Copy orking directory
COPY . /app

