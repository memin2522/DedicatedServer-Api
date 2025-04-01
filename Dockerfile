# Use an official Python runtime as the base image
FROM python:3.10-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file
COPY requirements.txt .
 
# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
 
# Copy the rest of the application code
COPY . .
 
# Expose the port that the Flask app will run on
EXPOSE 5000
 
# Command to run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]