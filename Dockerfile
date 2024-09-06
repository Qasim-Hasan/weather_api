# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app


# Copy requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container
COPY . /app/

# Expose the port your app runs on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
