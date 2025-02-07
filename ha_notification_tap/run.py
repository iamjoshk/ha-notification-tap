import logging
import os
import sys
import asyncio
from aiohttp import web, ClientSession, ClientTimeout
from contextlib import asynccontextmanager

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Configure logging to write to stdout without buffering
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger("notify_tap")

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

@asynccontextmanager
async def get_client_session():
    timeout = ClientTimeout(total=10)
    async with ClientSession(timeout=timeout) as session:
        yield session

async def handle_tap(request):
    event_data = request.match_info['event_data']
    print(f"Received tap event with data: {event_data}", flush=True)  # Direct print for immediate output
    logger.info(f"Processing tap event: {event_data}")
    
    try:
        async with get_client_session() as session:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            logger.debug(f"Sending event to {url}")
            
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                if response.status == 200:
                    logger.info(f"Successfully fired event with data: {event_data}")
                    return web.Response(text="Event fired", status=200)
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to fire event: {error_text}")
                    return web.Response(text=error_text, status=response.status)
    except Exception as e:
        logger.exception("Error processing tap event")
        return web.Response(text=f"Error: {str(e)}", status=500)

async def cleanup(app):
    logger.info("Cleaning up resources...")
    await asyncio.sleep(0.1)  # Allow pending tasks to complete

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)
app.on_cleanup.append(cleanup)

if __name__ == '__main__':
    print("Starting Notification Tap service...", flush=True)  # Direct print for immediate output
    logger.info("Initializing web server")
    web.run_app(
        app, 
        port=8099, 
        access_log=None,
        print=lambda s: print(s, flush=True)  # Force flush on server messages
    )
