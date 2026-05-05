FROM python:3.12-slim

# Install system dependencies for Flet
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Flet will run on
EXPOSE 7860

# We run it directly with python to avoid the flet-cli desktop dependency check
CMD ["python", "main.py"]