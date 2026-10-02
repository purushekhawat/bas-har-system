"""
Keep-Alive Cron Ping Script for Live Backend Hosting (Render / Railway / Cloud)
Prevents free backend cloud services from going to sleep after inactivity.
"""

import sys
import time
import urllib.request

DEFAULT_TARGET_URL = "http://127.0.0.1:8000/api/ping"

def ping_server(url: str):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BAS-KeepAlive-Cron/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] PING OK ({status}): {body.strip()}")
            return True
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] PING FAILED: {e}")
        return False

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET_URL
    print(f"Starting Keep-Alive Ping Service for: {target_url}")
    print("Press Ctrl+C to stop.")

    while True:
        ping_server(target_url)
        time.sleep(300)  # Ping every 5 minutes (300 seconds)
