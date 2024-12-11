import websockets, asyncio

async def client():
    async with websockets.connect("ws://localhost:5555") as websocket:
        await websocket.send("calculate")
        response = await websocket.recv()
        print(f"Server sent : {response}")

asyncio.run(client())