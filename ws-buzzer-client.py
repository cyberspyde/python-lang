import asyncio
import websockets
import keyboard

async def start_client():
    async with websockets.connect("ws://localhost:5555") as websocket:
        done = False
        while not done:
            if keyboard.is_pressed("shift"):
                await websocket.send("buzz")
                message = await websocket.recv()
                print(message)
                done = True

asyncio.run(start_client())