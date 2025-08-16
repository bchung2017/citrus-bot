# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

ENV OPENROUTER_API_KEY="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"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
