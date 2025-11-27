# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker-based synchronization service that fetches Audi vehicle location and battery data from the Audi Connect API and forwards it to a Traccar GPS tracking server using the OsmAnd protocol.

## Architecture

**audi_sync_daemon.py**: Main daemon that runs continuously in Docker, syncing at configured intervals. Uses environment variables for configuration.

The service uses the `audi_connect_ha` library (from https://github.com/arjenvrh/audi_connect_ha.git) to authenticate and fetch vehicle data from Audi's API.

### Data Flow
```
audi_sync_daemon.py → AudiConnectAccount (audi_connect_ha) → Audi Connect API
                                                                    ↓
Traccar Server ← HTTP GET (OsmAnd protocol) ← Vehicle State Parser
```

## Development

All Docker commands require `sudo` on this system.

```bash
# Build the image locally for development
sudo docker build -t audi-traccar-sync:dev .

# Or use docker-compose (pulls prebuilt image from ghcr.io)
sudo docker compose up -d

# View logs
sudo docker compose logs -f

# Stop the service
sudo docker compose down
```

## Configuration

Environment variables:
- `AUDI_USER`: Audi Connect email address (required)
- `AUDI_PASSWORD`: Audi Connect password (required)
- `AUDI_COUNTRY`: Country code for Audi Connect (default: DE)
- `TRACCAR_URL`: Traccar server endpoint (required - e.g., http://traccar.example.com:5055)
- `DEVICE_ID`: Unique identifier for the vehicle in Traccar (default: audi_ev)
- `SYNC_INTERVAL`: Seconds between sync attempts (default: 300 = 5 minutes)

For local development, these can be stored in `.env` (never commit this file). The `docker-compose.yml` has sensible defaults defined using the `${VAR:-default}` syntax.

## Traccar Integration

The service sends GPS data to Traccar using HTTP GET requests with these parameters:
- `id`: Device identifier
- `lat`, `lon`: GPS coordinates
- `timestamp`: Unix timestamp
- `battery`: State of charge (%)
- `charge`: Charging status (1 = charging, 0 = not charging)

Ensure the device with matching `id` exists in Traccar before starting the service.
