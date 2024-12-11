import asyncio, websockets, time

async def client(message):
    async with websockets.connect("ws://localhost:5555") as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        print(response)


while True:
    message = input("Input your message to Echo Websocket: ")
    asyncio.run(client(message))