import logging
import os
import sys
from aiohttp import web, ClientSession

# Configure logging to output to stderr for S6
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("notify_tap")

# Disable aiohttp access logging
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    logger.info(f"Received tap event with data: {event_data}")
    
    async with ClientSession() as session:
        try:
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

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    logger.info("Starting Notification Tap service")
    web.run_app(app, port=8099, access_log=None)
