# Audi to Traccar Sync

Docker container that automatically syncs your Audi location and battery data to Traccar GPS tracking server.

## Features

- Automatically fetches vehicle data from Audi Connect API
- Sends location and battery information to Traccar using OsmAnd protocol
- Configurable sync interval
- Runs as a background daemon in Docker
- Automatic restarts on failure

## Prerequisites

- Docker and Docker Compose installed
- Audi Connect account with an electric vehicle
- Traccar GPS tracking server running (default: http://localhost:5055)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd audi
   ```

2. **Copy the example environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` with your configuration**
   ```bash
   nano .env
   ```

   Configure the following variables:
   - `AUDI_USER` - Your Audi Connect email address
   - `AUDI_PASSWORD` - Your Audi Connect password
   - `AUDI_COUNTRY` - Country code (default: DE)
   - `TRACCAR_URL` - Your Traccar server URL (default: http://localhost:5055)
   - `DEVICE_ID` - Unique device identifier in Traccar (default: audi_ev)
   - `SYNC_INTERVAL` - Sync interval in seconds (default: 300 = 5 minutes)

4. **Build and start the container**
   ```bash
   sudo docker compose up -d
   ```

5. **Verify it's running**
   ```bash
   sudo docker compose ps
   sudo docker compose logs -f
   ```

## Configuration

All configuration is done via environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `AUDI_USER` | Audi Connect email | (required) |
| `AUDI_PASSWORD` | Audi Connect password | (required) |
| `AUDI_COUNTRY` | Country code | `DE` |
| `TRACCAR_URL` | Traccar server URL | `http://localhost:5055` |
| `DEVICE_ID` | Device identifier in Traccar | `audi_ev` |
| `SYNC_INTERVAL` | Sync interval in seconds | `300` (5 minutes) |

**Important:** Make sure the device with ID matching `DEVICE_ID` exists in your Traccar server before starting the sync.

## Management

```bash
# View logs (follow mode)
sudo docker compose logs -f

# View last 50 lines
sudo docker compose logs --tail 50

# Restart the container
sudo docker compose restart

# Stop the container
sudo docker compose down

# Rebuild after code changes
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

## Data Sent to Traccar

The service sends the following data to Traccar via HTTP GET (OsmAnd protocol):

- **id**: Device identifier
- **lat**: Latitude
- **lon**: Longitude
- **timestamp**: Unix timestamp
- **speed**: Speed (currently 0 as vehicle is typically parked)
- **battery**: State of charge in percentage
- **charge**: Charging status (1 = charging, 0 = not charging)

## Troubleshooting

### Container keeps restarting

Check the logs for errors:
```bash
sudo docker compose logs --tail 100
```

Common issues:
- Invalid Audi Connect credentials
- Traccar server not accessible
- Missing device ID in Traccar

### Container can't connect to Traccar

The container uses `network_mode: "host"` to access Traccar on localhost. If your Traccar server runs elsewhere:

1. Update `TRACCAR_URL` in `.env` to point to your Traccar server
2. Consider removing `network_mode: "host"` from `docker-compose.yml` if not needed

## Architecture

- **audi_sync_daemon.py**: Main sync daemon that runs continuously
- **homeassistant_stub.py**: Stub module that provides minimal Home Assistant compatibility for the audi_connect_ha library
- **Dockerfile**: Builds the container image with all dependencies
- **docker-compose.yml**: Defines the service configuration

The service uses the [audi_connect_ha](https://github.com/arjenvrh/audi_connect_ha) library to communicate with Audi's API.

## License

See LICENSE file for details.
