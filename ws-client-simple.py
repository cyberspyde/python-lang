import asyncio
import websockets

async def hello():
    uri = "ws://100.104.246.114:8765"
    async with websockets.connect(uri) as websocket:
        name = input("Please enter your name")

        await websocket.send(name)
        print(f"Client sent: {name}")

        greeting = await websocket.recv()
        print(f"Client received: {greeting}")

asyncio.run(hello())