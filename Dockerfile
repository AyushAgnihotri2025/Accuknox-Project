# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables to ensure Python output is displayed in the console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory inside the container
WORKDIR /AccuknoxProject

# Copy the requirements file into the container
COPY requirements.txt /AccuknoxProject

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /AccuknoxProject

# Copy the entrypoint script into the container
COPY entrypoint.sh /AccuknoxProject

# Make the entrypoint script executable
RUN chmod +x /AccuknoxProject/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/AccuknoxProject/entrypoint.sh"]