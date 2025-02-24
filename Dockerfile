# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "server.py"]

COPY career_trends.db /app/career_trends.db



