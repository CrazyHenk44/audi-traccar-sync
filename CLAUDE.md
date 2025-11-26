# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker-based synchronization service that fetches Audi vehicle location and battery data from the Audi Connect API and forwards it to a Traccar GPS tracking server using the OsmAnd protocol.

## Architecture

The service consists of two main components:

1. **audi_sync_daemon.py** (production): A daemon that runs continuously in Docker, syncing at configured intervals. Uses environment variables for configuration.

2. **audi_to_traccar.py** (standalone/testing): A one-shot script that requires `AudiAPI/credentials.json`. This is legacy code primarily for local testing.

Both scripts use the `audi_connect_ha` library (from https://github.com/arjenvrh/audi_connect_ha.git) to authenticate and fetch vehicle data from Audi's API.

### Data Flow
```
audi_sync_daemon.py → AudiConnectAccount (audi_connect_ha) → Audi Connect API
                                                                    ↓
Traccar Server ← HTTP GET (OsmAnd protocol) ← Vehicle State Parser
```

## Docker Commands

All Docker commands require `sudo` on this system.

```bash
# Build the image
sudo docker compose build

# Start the service
sudo docker compose up -d

# View logs (follow mode)
sudo docker compose logs -f

# Stop the service
sudo docker compose down

# Rebuild from scratch (e.g., to update audi_connect_ha library)
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

## Configuration

All configuration is stored in `.env` (never commit this file). Copy from `.env.example`:
```bash
cp .env.example .env
```

Environment variables:
- `AUDI_USER`: Audi Connect email address (required)
- `AUDI_PASSWORD`: Audi Connect password (required)
- `AUDI_COUNTRY`: Country code for Audi Connect (default: DE)
- `TRACCAR_URL`: Traccar server endpoint (default: http://localhost:5055)
- `DEVICE_ID`: Unique identifier for the vehicle in Traccar (default: audi_ev)
- `SYNC_INTERVAL`: Seconds between sync attempts (default: 300 = 5 minutes)

These are all configurable via `.env` and have sensible defaults defined in `docker-compose.yml` using the `${VAR:-default}` syntax.

## Network Configuration

The container uses `network_mode: "host"` to access Traccar on localhost. If Traccar runs in a different container or remote server, modify `TRACCAR_URL` accordingly.

## Traccar Integration

The service sends GPS data to Traccar using HTTP GET requests with these parameters:
- `id`: Device identifier
- `lat`, `lon`: GPS coordinates
- `timestamp`: Unix timestamp
- `battery`: State of charge (%)
- `charge`: Charging status (1 = charging, 0 = not charging)

Ensure the device with matching `id` exists in Traccar before starting the service.
