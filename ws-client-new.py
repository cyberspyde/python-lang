import asyncio
import websockets

# Function to handle the chat client
async def chat():
    async with websockets.connect('ws://localhost:5555') as websocket:
        await websocket.send("calculate")
        response = await websocket.recv()
        print(f"Got : {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(chat())