import logging
import os
from aiohttp import web, ClientSession

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prevent aiohttp access logging
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    
    async with ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                if response.status == 200:
                    return web.Response(text="Event fired", status=200)
                else:
                    return web.Response(text=await response.text(), status=response.status)
        except Exception as e:
            return web.Response(text=f"Error: {str(e)}", status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    web.run_app(app, port=8099, print=logger.info, access_log=None)
