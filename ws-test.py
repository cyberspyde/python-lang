import websockets, asyncio, time

class WebSocket():
    def __init__(self, host="localhost", port=5555):
        self.clients = set()
        self.host = host
        self.port = port
        self.task = 0
    
    async def long_calculation(self):
        return sum(i * i for i in range(100000000))

    async def handle_client(self, websocket):
        self.clients.add(websocket)
        self.task += 1
        try:
            async for message in websocket:
                if message == "calculate":
                    start_time = time.time()
                    response = await self.long_calculation()
                    end_time = time.time()
                    await websocket.send(str(response))
                print(f"Processing Took : {end_time - start_time:.4f}")        
            self.clients.remove(websocket)
            self.task -= 1
            print(f"Tasks remaining : {self.task} \nClients Remaining : {len(self.clients)}")
        except websockets.exceptions.ConnectionClosed:
            print("Connecetion Closed")

    async def start_server(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

    
ws = WebSocket()
asyncio.run(ws.start_server())