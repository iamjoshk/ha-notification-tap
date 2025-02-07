import os
from aiohttp import web, ClientSession, ClientTimeout

# Home Assistant Supervisor and API endpoints
SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
CORE_API = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    
    async with ClientSession() as session:
        try:
            # Use proper Home Assistant authentication
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            # Use Core API to fire event
            url = f"{CORE_API}/events/{EVENT_TYPE}"
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
