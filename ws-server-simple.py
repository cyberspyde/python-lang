import websockets
import asyncio

async def hello(websocket):
    name = await websocket.recv()
    print(f"Server got : {name}")
    greeting = f"Hello {name}"

    await websocket.send(greeting)
    print(f"Server sent {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
