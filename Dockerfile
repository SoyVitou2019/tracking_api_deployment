# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install system dependencies for TensorFlow with GPU support
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    wget \
    ca-certificates \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . /code

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application

# Create a virtual environment named 'venv'
RUN python3.11 -m venv venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

# Install the required packages from requirements.txt inside the virtual environment
RUN pip install -r /code/requirements.txt
# Install TensorFlow with GPU support
RUN pip install tensorflow[extra,gpu]
# RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
