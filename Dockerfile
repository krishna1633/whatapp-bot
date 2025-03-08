# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy language model
RUN python3.10 -m spacy download en_core_web_sm

# Copy app files
COPY . .

# Expose port for API server
EXPOSE 8080

# Start the server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "server:app"]
