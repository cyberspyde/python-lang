import websockets, asyncio, time

class WSServer():
    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port

    async def client_handler(self, websocket):
        async for message in websocket:
            await websocket.send(f"You sent: {message}")
            
        print(f"Current clients count : {len(self.clients)}")
    async def start_server(self):
        async with websockets.serve(self.client_handler, self.host, self.port) as websocket:
            await websocket.serve_forever()

ws = WSServer()
asyncio.run(ws.start_server())