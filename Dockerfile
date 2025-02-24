# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Ensure pickle file is copied inside the container
COPY career_trends.pkl /app/career_trends.pkl

# Run the Flask app
CMD ["python", "server.py"]



