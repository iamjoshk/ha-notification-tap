import logging
import os
import sys
from aiohttp import web, ClientSession

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    logger.info(f"Received tap event: {event_data}")
    
    async with ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                if response.status == 200:
                    logger.info(f"Event fired: {event_data}")
                    return web.Response(text="OK", status=200)
                else:
                    error_text = await response.text()
                    logger.error(f"Error: {error_text}")
                    return web.Response(text=error_text, status=response.status)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return web.Response(text=str(e), status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    logger.info("Starting server on port 8099")
    web.run_app(app, port=8099, print=None)
