FROM ghcr.io/unitvectory-labs/adk-docker-base:latest

WORKDIR /app

# Copy the requirements file first to leverage Docker cache
# This will install the latest version of "google-adk"
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

COPY family_agent/ ./family_agent/

EXPOSE 8000

# Run the Web UI for ADK
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
