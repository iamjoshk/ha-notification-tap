import os
import asyncio
from aiohttp import web, ClientSession, ClientTimeout, TCPConnector

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    
    timeout = ClientTimeout(total=10)
    connector = TCPConnector(force_close=True)
    
    async with ClientSession(timeout=timeout, connector=connector) as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                if response.status == 200:
                    return web.Response(text="OK", status=200)
                return web.Response(text=await response.text(), status=response.status)
        except Exception as e:
            return web.Response(text=str(e), status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    web.run_app(app, port=8099, print=None, access_log=None)
