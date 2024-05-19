FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Set up the virtual environment and install Python packages
RUN python -m venv myenv
RUN /bin/bash -c "source myenv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Copy the rest of the application code
COPY . /code

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["/bin/bash", "-c", "source myenv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8000"]
