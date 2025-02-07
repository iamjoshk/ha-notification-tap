import os
import sys
import json
from aiohttp import web, ClientSession
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)

# Load config
try:
    with open('/data/options.json') as f:
        config = json.load(f)
        HA_TOKEN = config.get('ha_token')
        # Use supervisor's internal URL
        HA_URL = "http://supervisor/core/api"
except Exception as e:
    log(f"[ERROR] Failed to load config: {e}")
    HA_TOKEN = None
    HA_URL = "http://supervisor/core/api"

EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    try:
        # Get event data from query or path
        if request.query_string:
            event_data = dict(request.query)
        else:
            event_data = {"data": request.match_info.get('event_data', '')}
        
        log(f"[DEBUG] Processing event: {event_data}")
        
        # Call HA API directly
        async with ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            async with session.post(url, headers=headers, json=event_data) as response:
                if response.status == 200:
                    log("[INFO] Event fired successfully")
                    return web.Response(text="OK", status=200)
                log(f"[ERROR] Failed to fire event: {await response.text()}")
                return web.Response(text="Failed to fire event", status=response.status)
    except Exception as e:
        log(f"[ERROR] {str(e)}")
        return web.Response(text=str(e), status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)
app.router.add_get('/api/notify-tap', handle_tap)

if __name__ == '__main__':
    log(f"[INFO] Starting server on port 8099")
    log(f"[INFO] Using HA URL: {HA_URL}")
    web.run_app(app, port=8099, print=None, access_log=None)
