import os
import sys
import asyncio
from aiohttp import web, ClientSession, ClientTimeout, TCPConnector

def log(message):
    print(message, file=sys.stderr, flush=True)

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN')
HA_URL = "http://supervisor/core/api"
EVENT_TYPE = "notification_tap_event"

async def handle_tap(request):
    event_data = request.match_info['event_data']
    log(f"Received tap event: {event_data}")
    
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
                    log(f"Successfully fired event: {event_data}")
                    return web.Response(text="OK", status=200)
                log(f"Error firing event: {await response.text()}")
                return web.Response(text=await response.text(), status=response.status)
        except Exception as e:
            log(f"Error: {str(e)}")
            return web.Response(text=str(e), status=500)

async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8099)
    await site.start()

app = web.Application()
app.router.add_get('/api/notify-tap/{event_data}', handle_tap)

if __name__ == '__main__':
    log("Starting Notification Tap service...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    log("Server running on port 8099")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
