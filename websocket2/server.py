import asyncio
import websockets
import cv2
import numpy as np
import mss
from queue import Queue

HOST = "localhost"

PORT = 8766


async def server(websocket, path):
    monitor = {
        'top': 0,
        'left': 0,
        'width': 640,
        'height': 480
    }
    while True:
        # Capture a screenshot of the entire screen
        with mss.mss() as sct:
            screenshot = sct.shot(output='1')
            raw = sct.grab(monitor)
            # raw = sct.shot()
        # Convert the screenshot to a NumPy array
        frame = np.array(raw)
        # params = [cv2.IMWRITE_JPEG_QUALITY, 50, cv2.IMWRITE_JPEG_OPTIMIZE, 1]

        # Encode the frame (e.g., as JPEG)
        _, encoded_frame = cv2.imencode('.jpg', frame)

        # Convert the encoded frame to bytes
        frame_bytes = encoded_frame.tobytes()

        # Send the frame over the WebSocket connection
        await websocket.send(frame_bytes)


async def start_server():
    async with websockets.serve(server, HOST, PORT):
        await asyncio.Future()


class WebsocketServer:
    def __init__(self, queue, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.monitor = None
        self.queue = queue

    async def loop(self, websocket, path):
        '''start screen share loop'''
        while True:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                raw = sct.grab(monitor)
            frame = np.array(raw, np.uint8)
            _, encoded_frame = cv2.imencode('.jpg', frame)
            frame_bytes = encoded_frame.tobytes()
            await websocket.send(frame_bytes)

    async def game_loop(self, websocket, path):
        '''start game share loop'''
        while True:
            print('забота')
            image = await self.queue.get()
            if not image:
                print('нет изображения')
                await websocket.send("нет изображения")
            await websocket.send(image)

    async def start(self, loop=None):
        async with websockets.serve(self.loop if loop is None else self.game_loop, self.host, self.port):
            await asyncio.Future()


if __name__ == "__main__":

    q = Queue()
    serv = WebsocketServer(q, HOST, PORT)
    asyncio.run(serv.start())