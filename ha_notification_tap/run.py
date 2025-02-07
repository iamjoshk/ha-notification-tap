import os
import sys
from aiohttp import web, ClientSession, ClientTimeout
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
CORE_API = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    log(f"[DEBUG] Received request: {request.url}")
    log(f"[DEBUG] Event data: {event_data}")
    
    async with ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{CORE_API}/events/{EVENT_TYPE}"
            log(f"[DEBUG] Sending event to: {url}")
            log(f"[DEBUG] Token exists: {bool(SUPERVISOR_TOKEN)}")
            
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                response_text = await response.text()
                log(f"[DEBUG] Response status: {response.status}")
                log(f"[DEBUG] Response body: {response_text}")
                
                if response.status == 200:
                    return web.Response(text="OK", status=200)
                return web.Response(text=response_text, status=response.status)
        except Exception as e:
            log(f"[DEBUG] Error: {str(e)}")
            return web.Response(text=str(e), status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    log("[DEBUG] Starting server on port 8099")
    log("[DEBUG] Waiting for requests...")
    web.run_app(app, port=8099, print=None, access_log=None)
