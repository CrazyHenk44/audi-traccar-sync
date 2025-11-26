#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import requests
import os
import sys
import time
from datetime import datetime

# Import homeassistant stub before audi_connect_ha to satisfy dependencies
import homeassistant_stub

sys.path.insert(0, '/app')
from audi_connect_ha.custom_components.audiconnect.audi_connect_account import AudiConnectAccount

# Configuration from environment variables
TRACCAR_URL = os.getenv('TRACCAR_URL', 'http://host.docker.internal:5055')
DEVICE_ID = os.getenv('DEVICE_ID', 'audi_ev')
SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', '300'))  # Default 5 minutes
AUDI_USER = os.getenv('AUDI_USER')
AUDI_PASSWORD = os.getenv('AUDI_PASSWORD')
AUDI_COUNTRY = os.getenv('AUDI_COUNTRY', 'DE')

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

async def get_audi_data():
    """Fetch data from Audi API"""
    if not AUDI_USER or not AUDI_PASSWORD:
        print("✗ Missing AUDI_USER or AUDI_PASSWORD environment variables")
        return None

    async with aiohttp.ClientSession() as session:
        account = AudiConnectAccount(session, AUDI_USER, AUDI_PASSWORD, AUDI_COUNTRY, None, 1)
        await account.login()

        if account._loggedin:
            print("✓ Login successful!")

            # Fetch vehicle information
            await account.update(None)

            # Get the first vehicle's data
            if account._vehicles:
                vehicle = account._vehicles[0]
                return vehicle._vehicle.state
            else:
                print("✗ No vehicles found")
                return None
        else:
            print("✗ Login failed")
            return None

def send_to_traccar(vehicle_data):
    """Send GPS data to Traccar using OsmAnd protocol"""
    if not vehicle_data or 'position' not in vehicle_data:
        print("✗ No position data available")
        return False

    position = vehicle_data['position']

    # Prepare parameters for Traccar
    timestamp = position['timestamp']
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    params = {
        'id': DEVICE_ID,
        'lat': position['latitude'],
        'lon': position['longitude'],
        'timestamp': int(timestamp.timestamp()),
        'speed': 0,  # Vehicle is parked
        'battery': vehicle_data.get('stateOfCharge', 0),
        'charge': 1 if vehicle_data.get('chargingState') not in ['notReadyForCharging', 'off'] else 0
    }

    try:
        response = requests.get(TRACCAR_URL, params=params, timeout=10)
        if response.status_code == 200:
            print(f"✓ Data sent to Traccar successfully")
            print(f"  Location: {params['lat']}, {params['lon']}")
            print(f"  Battery: {params['battery']}%")
            print(f"  Timestamp: {position['timestamp']}")
            return True
        else:
            print(f"✗ Traccar returned status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending to Traccar: {e}")
        return False

async def sync_once():
    """Perform one sync cycle"""
    print(f"--- Audi to Traccar Sync ---")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Traccar URL: {TRACCAR_URL}")
    print(f"Device ID: {DEVICE_ID}\n")

    # Get data from Audi
    vehicle_data = await get_audi_data()

    if vehicle_data:
        # Send to Traccar
        send_to_traccar(vehicle_data)
    else:
        print("✗ Failed to get vehicle data")

    print(f"--- Sync Complete ---\n")

async def main():
    """Main daemon loop"""
    print("="*50)
    print("Audi to Traccar Sync Daemon")
    print("="*50)
    print(f"Sync interval: {SYNC_INTERVAL} seconds ({SYNC_INTERVAL/60:.1f} minutes)")
    print(f"Audi user: {AUDI_USER if AUDI_USER else 'NOT SET'}")
    print(f"Audi country: {AUDI_COUNTRY}")
    print("="*50)
    print()

    while True:
        try:
            await sync_once()
        except Exception as e:
            print(f"✗ Error during sync: {e}")
            import traceback
            traceback.print_exc()

        # Wait for next sync
        print(f"Sleeping for {SYNC_INTERVAL} seconds...")
        print()
        await asyncio.sleep(SYNC_INTERVAL)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)
