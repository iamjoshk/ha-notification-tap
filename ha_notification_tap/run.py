import os
import sys
import json
import asyncio
import logging
from aiohttp import web, ClientSession, ClientTimeout, TCPConnector

# Load config
with open('/data/options.json') as config_file:
    config = json.load(config_file)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG if config.get('debug', False) else logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('notify_tap')

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    logger.debug(f"Received tap with data: {event_data}")
    logger.debug(f"Supervisor token exists: {bool(SUPERVISOR_TOKEN)}")
    
    timeout = ClientTimeout(total=10)
    connector = TCPConnector(force_close=True)
    
    async with ClientSession(timeout=timeout, connector=connector) as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            logger.debug(f"Sending event to: {url}")
            logger.debug(f"Event data: {{'data': {event_data}}}")
            
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                response_text = await response.text()
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response text: {response_text}")
                
                if response.status == 200:
                    return web.Response(text="OK", status=200)
                return web.Response(text=response_text, status=response.status)
        except Exception as e:
            logger.debug(f"Error occurred: {str(e)}")
            return web.Response(text=str(e), status=500)

async def cleanup_background_tasks(app):
    for task in set(asyncio.all_tasks()):
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == '__main__':
    logger.info("Starting Notification Tap service...")
    if config.get('debug', False):
        logger.info("Debug logging enabled")
    web.run_app(app, port=8099, access_log=logger if config.get('debug', False) else None, print=logger.info)
