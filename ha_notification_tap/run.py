from aiohttp import web, ClientSession
import os

# No logging setup - use print directly

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    print(f"Received tap event: {event_data}")
    
    async with ClientSession() as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                if response.status == 200:
                    print(f"Event fired: {event_data}")
                    return web.Response(text="OK", status=200)
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return web.Response(text=error_text, status=response.status)
        except Exception as e:
            print(f"Error: {str(e)}")
            return web.Response(text=str(e), status=500)

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

# Simple start with no logging output
runner = web.AppRunner(app)

async def start():
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8099)
    await site.start()
    print("Server started on port 8099")

web.run_app(app, port=8099, print=None, access_log=None)
