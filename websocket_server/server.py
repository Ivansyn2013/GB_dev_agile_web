import websockets
import asyncio
import pygame

EVENT = pygame.event.custom_type()

HOST = "127.0.0.1"
PORT = 6677

async def handler(websocket, path):
    async for message in websocket:
        await processMsg(message)
        await websocket.send("success")

async def processMsg(message):
    print(f"[Resived]: {message}")
    pygame.fastevent.post(pygame.event.Event(EVENT, message=message))

async def main(future):
    async with websockets.serve(handler, HOST, PORT):
        await future


if __name__ == "__main__":
    asyncio.run(main())
