import os
import sys
from aiohttp import web, ClientSession, ClientTimeout
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)

# Get supervisor token and validate
SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
if not SUPERVISOR_TOKEN:
    log("[ERROR] No Supervisor token found! Make sure hassio_api and auth_api are enabled in config.yaml")
    sys.exit(1)

# Use correct Home Assistant API URL
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    try:
        # Get data from query parameters or path
        if request.query_string:
            # Handle URL query parameters
            event_data = dict(request.query)
            log(f"[DEBUG] Query parameters received: {event_data}")
        elif request.method == 'POST':
            # Handle POST data
            data = await request.json()
            event_data = data
            log(f"[DEBUG] POST data received: {event_data}")
        else:
            # Handle path parameter
            event_data = {"data": request.match_info['event_data']}
            log(f"[DEBUG] Path parameter received: {event_data}")
            
        log(f"[DEBUG] Processing event data: {event_data}")
        # Add HTTPS detection
        if request.headers.get('X-Forwarded-Proto') == 'https' or \
           request.url.scheme == 'https':
            log("[ERROR] HTTPS request detected - this add-on only supports HTTP")
            return web.Response(
                text="This add-on only supports HTTP, not HTTPS. Please use http:// in your URL.",
                status=400
            )
        
        log(f"[DEBUG] Full URL: {request.url}")
        log(f"[DEBUG] Headers: {dict(request.headers)}")
        log(f"[DEBUG] Query String: {request.query_string}")
        log(f"[DEBUG] Remote: {request.remote}")
        log(f"[DEBUG] Received request: {request.url}")
        log(f"[DEBUG] Event data: {event_data}")
    
        async with ClientSession() as session:
            try:
                headers = {
                    "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                    "Content-Type": "application/json",
                }
            
                # Log full request details for debugging
                url = f"{HA_URL}/events/{EVENT_TYPE}"
                log(f"[DEBUG] Full request details:")
                log(f"[DEBUG] URL: {url}")
                log(f"[DEBUG] Headers: {headers}")
                log(f"[DEBUG] Data: {{'data': {event_data}}}")
            
                async with session.post(url, headers=headers, json={"data": event_data}) as response:
                    response_text = await response.text()
                    log(f"[DEBUG] Response status: {response.status}")
                    log(f"[DEBUG] Response headers: {dict(response.headers)}")
                    log(f"[DEBUG] Response body: {response_text}")
                
                    if response.status == 200:
                        log("[INFO] Event fired successfully")
                        return web.Response(text="OK", status=200)
                    log("[ERROR] Failed to fire event")
                    return web.Response(text=response_text, status=response.status)
            except Exception as e:
                log(f"[ERROR] Exception: {str(e)}")
                return web.Response(text=str(e), status=500)
    except Exception as e:
        log(f"[ERROR] Exception: {str(e)}")
        return web.Response(text=str(e), status=500)

app = web.Application()
# Add routes that handle both styles
app.router.add_get('/api/notify-tap', handle_tap)  # For query parameters
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)  # For path parameters
app.router.add_post('/api/notify-tap', handle_tap)

if __name__ == '__main__':
    log("[DEBUG] Starting server on port 8099")
    log("[DEBUG] Host networking enabled - server will be accessible on all network interfaces")
    log("[DEBUG] Try accessing: http://YOUR_HA_IP:8099/api/notify-tap/test")
    web.run_app(
        app,
        host='0.0.0.0',  # Listen on all interfaces
        port=8099,
        print=None,
        access_log=None
    )
