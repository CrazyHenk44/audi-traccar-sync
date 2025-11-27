# Audi to Traccar Sync

Automatically sync your Audi vehicle location and battery data to a Traccar GPS tracking server.

## Quick Start

### Option 1: Single Docker Command

```bash
docker run -d \
  --name audi-traccar-sync \
  --restart unless-stopped \
  -e AUDI_USER="your.email@example.com" \
  -e AUDI_PASSWORD="your_password" \
  -e AUDI_COUNTRY="DE" \
  -e TRACCAR_URL="http://your-traccar-server:5055" \
  -e DEVICE_ID="audi_ev" \
  -e SYNC_INTERVAL="300" \
  ghcr.io/crazyhenk44/audi-traccar-sync:main
```

### Option 2: Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  audi-sync:
    image: ghcr.io/crazyhenk44/audi-traccar-sync:main
    container_name: audi-traccar-sync
    restart: unless-stopped
    environment:
      - AUDI_USER=your.email@example.com
      - AUDI_PASSWORD=your_password
      - AUDI_COUNTRY=DE
      - TRACCAR_URL=http://your-traccar-server:5055
      - DEVICE_ID=audi_ev
      - SYNC_INTERVAL=300
```

Then run:
```bash
docker compose up -d
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDI_USER` | Audi Connect email | (required) |
| `AUDI_PASSWORD` | Audi Connect password | (required) |
| `AUDI_COUNTRY` | Country code | `DE` |
| `TRACCAR_URL` | Traccar server URL | (required) |
| `DEVICE_ID` | Device identifier in Traccar | `audi_ev` |
| `SYNC_INTERVAL` | Sync interval in seconds | `300` |

**Note:** Create the device in Traccar with the matching `DEVICE_ID` before starting the sync.

## Useful Commands

```bash
# View logs
docker logs -f audi-traccar-sync

# Restart
docker restart audi-traccar-sync

# Stop
docker stop audi-traccar-sync
```

Or with Docker Compose:
```bash
docker compose logs -f
docker compose restart
docker compose down
```

## What Gets Synced

- GPS coordinates (latitude/longitude)
- Battery level (%)
- Charging status
- Timestamp

Data is sent to Traccar using the OsmAnd protocol.
