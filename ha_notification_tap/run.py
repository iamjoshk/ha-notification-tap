import os
import asyncio
from aiohttp import web, ClientSession, ClientTimeout, TCPConnector

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    print(f"DEBUG: Received tap with data: {event_data}")
    print(f"DEBUG: Supervisor token exists: {bool(SUPERVISOR_TOKEN)}")
    
    timeout = ClientTimeout(total=10)
    connector = TCPConnector(force_close=True)
    
    async with ClientSession(timeout=timeout, connector=connector) as session:
        try:
            headers = {
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            }
            
            url = f"{HA_URL}/events/{EVENT_TYPE}"
            print(f"DEBUG: Sending event to: {url}")
            print(f"DEBUG: Event data: {{'data': {event_data}}}")
            
            async with session.post(url, headers=headers, json={"data": event_data}) as response:
                response_text = await response.text()
                print(f"DEBUG: Response status: {response.status}")
                print(f"DEBUG: Response text: {response_text}")
                
                if response.status == 200:
                    return web.Response(text="OK", status=200)
                return web.Response(text=response_text, status=response.status)
        except Exception as e:
            print(f"DEBUG: Error occurred: {str(e)}")
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
    web.run_app(app, port=8099, access_log=None)
