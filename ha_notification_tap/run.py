import json
import logging
import os
from aiohttp import web, ClientSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"

async def handle_tap(request):
    action_id = request.match_info['action_id']
    
    try:
        with open('/data/options.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        return web.Response(text=f"Error loading config: {str(e)}", status=500)

    # Get event data for this action
    event_data = config['actions'].get(action_id)
    if not event_data:
        return web.Response(text=f"Action {action_id} not found", status=404)

    # Add action_id to event data
    event_data = {**event_data, 'action_id': action_id}

    async with ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{config['event_type']}"
            async with session.post(url, headers=headers, json=event_data) as response:
                if response.status == 200:
                    return web.Response(text="Event fired", status=200)
                else:
                    return web.Response(text=await response.text(), status=response.status)
        except Exception as e:
            return web.Response(text=f"Error: {str(e)}", status=500)

app = web.Application()
app.router.add_get('/deep-link-to-ha-notify-tap-addon/{action_id}', handle_tap)

if __name__ == '__main__':
    web.run_app(app, port=8099)
