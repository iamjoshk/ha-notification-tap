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
        HA_HOST = config.get('ha_host', 'homeassistant')
        REDIRECT_URL = config.get('redirect_url', 'homeassistant://navigate/lovelace/0')
        # Add /api to base URL
        HA_URL = f"http://{HA_HOST}:8123/api"
        log(f"[DEBUG] Config loaded - Host: {HA_HOST}, Token: {'Present' if HA_TOKEN else 'Missing'}")
except Exception as e:
    log(f"[ERROR] Failed to load config: {e}")
    sys.exit(1)

EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    try:
        log("[DEBUG] ====== New Request ======")
        log(f"[DEBUG] Method: {request.method}")
        log(f"[DEBUG] URL: {request.url}")
        log(f"[DEBUG] Headers: {dict(request.headers)}")
        log(f"[DEBUG] Query: {request.query_string}")

        # Get event data from query or path
        if request.query_string:
            event_data = dict(request.query)
        else:
            event_data = {"data": request.match_info.get('event_data', '')}
        
        log(f"[DEBUG] Processing event: {event_data}")
        
        # Check if request is from mobile browser
        user_agent = request.headers.get('User-Agent', '').lower()
        is_mobile = 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent
        
        async with ClientSession() as session:
            if not HA_TOKEN:
                raise ValueError("Missing HA token")

            headers = {
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json",
            }
            
            # Construct proper API URL
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            log(f"[DEBUG] Full request details:")
            log(f"[DEBUG] URL: {url}")
            log(f"[DEBUG] Headers: {headers}")
            log(f"[DEBUG] Data: {event_data}")
            
            # Use POST to match HA API
            async with session.post(url, headers=headers, json=event_data) as response:
                response_text = await response.text()
                log(f"[DEBUG] Response ({response.status}): {response_text}")
                
                if response.status == 404:
                    log("[ERROR] API endpoint not found - check URL format")
                    return web.Response(text="API endpoint not found", status=404)
                elif response.status == 401:
                    log("[ERROR] Unauthorized - check HA token")
                    return web.Response(text="Unauthorized", status=401)
                
                if response.status == 200:
                    log("[INFO] Event fired successfully")
                    return web.Response(
                        status=302,
                        headers={
                            'Location': REDIRECT_URL,
                            'Cache-Control': 'no-cache'
                        }
                    )
                    
                log(f"[ERROR] Failed to fire event: {response_text}")
                return web.Response(text="Failed to fire event", status=response.status)
    except Exception as e:
        log(f"[ERROR] {str(e)}")
        return web.Response(text=str(e), status=500)

app = web.Application()
# Support both GET and POST
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)
app.router.add_get('/api/notify-tap', handle_tap)
app.router.add_post('/api/notify-tap/{event_data}', handle_tap)
app.router.add_post('/api/notify-tap', handle_tap)

if __name__ == '__main__':
    log(f"[INFO] Starting server on port 8099")
    log(f"[INFO] Using HA URL: {HA_URL}")
    web.run_app(app, port=8099, print=None, access_log=None)
