# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python packages from requirements.txt
RUN pip install --no-cache-dir --timeout 1000 -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the Flask app will run on
EXPOSE 6000

# Set environment variables if necessary
# ENV ENV_VARIABLE_NAME=value

# Run the Flask app when the container launches
CMD ["python", "main.py"]
