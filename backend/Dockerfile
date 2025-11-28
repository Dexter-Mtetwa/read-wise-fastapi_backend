# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Railway will use (Railway sets this automatically)
ENV PORT=8000

# Command to run the app
# Use JSON array format for better signal handling
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]