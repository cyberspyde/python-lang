import websockets
import asyncio

clients = []

async def handler(websocket):
    global clients
    global fastest_time

    message = await websocket.recv()

    if message == "buzz":
        response_time = asyncio.get_event_loop().time()
        clients.append([websocket, response_time])

        if len(clients) == 1:
            await websocket.send("Youre the first")
            fastest_time = response_time
        else:
            t = round(response_time - fastest_time, 2)
            await websocket.send(f"Responded {t} seconds slower")


async def start_server():
    async with websockets.serve(handler, "localhost", 5555):
        print("Websocket started")
        await asyncio.Future()

asyncio.run(start_server())