import asyncio
from websocket_server.server import main
import threading
import pygame


def start_server(loop, future):
    loop.run_until_complete(main(future))

def stop_server(loop, future):
    loop.call_soon_threadsafe(future.set_result, None)


loop = asyncio.get_event_loop()
future = loop.create_future()

thread = threading.Thread(target=start_server, args=(loop, future))
thread.start()