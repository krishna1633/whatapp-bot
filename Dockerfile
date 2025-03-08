# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY . .

# Expose port for API server
EXPOSE 8080

# Start the server using Gunicorn
CMD ["python3.10", "server.py"]
