import websockets, asyncio, time

class WebSocket():
    def __init__(self, host="localhost", port=5555):
        self.host = host
        self.port = port
        self.clients = set()

    async def longCalculation(self):
        await asyncio.sleep(5)
        return sum(i * i for i in range(100000))

    async def handle_client(self, websocket):
        async for message in websocket:
            if message == "calculate":
                start_time = time.time()
                response = await self.longCalculation()
                end_time = time.time()

                websocket.send(response)
            print(f"Processing took : {end_time - start_time:.4f}")

    async def start_server(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()
    

ws = WebSocket()
asyncio.run(ws.start_server())