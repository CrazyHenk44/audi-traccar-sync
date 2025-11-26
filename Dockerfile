FROM python:3.11-slim

WORKDIR /app

# Install git to clone the repository
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the audi_connect_ha library
RUN git clone https://github.com/arjenvrh/audi_connect_ha.git /app/audi_connect_ha

# Install required Python packages
RUN pip install --no-cache-dir \
    aiohttp \
    requests \
    beautifulsoup4 \
    voluptuous

# Copy the sync script and homeassistant stub
COPY audi_sync_daemon.py /app/
COPY homeassistant_stub.py /app/

# Set environment variables for configuration
ENV TRACCAR_URL=http://host.docker.internal:5055 \
    DEVICE_ID=audi_ev \
    SYNC_INTERVAL=300

CMD ["python", "-u", "audi_sync_daemon.py"]
