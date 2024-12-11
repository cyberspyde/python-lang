import asyncio
import websockets
import json

# Global state to track connected clients and their drawing actions
clients = set()
drawing_history = []

async def handle_connection(websocket, path):
    # Add this client to the set of connected clients
    clients.add(websocket)
    
    try:
        # Send existing drawing history to the new client
        await websocket.send(json.dumps({
            'type': 'history',
            'drawing': drawing_history
        }))

        # Listen for messages from this client
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'draw':
                # Store and broadcast drawing action to all other clients
                drawing_history.append(data['drawing'])
                await broadcast_drawing(data['drawing'], websocket)
            
            elif data['type'] == 'clear':
                # Clear the entire drawing board
                drawing_history.clear()
                await broadcast_clear(websocket)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Remove client when connection closes
        clients.remove(websocket)

async def broadcast_drawing(drawing, sender):
    # Send drawing to all clients except the sender
    for client in clients:
        if client != sender:
            await client.send(json.dumps({
                'type': 'draw',
                'drawing': drawing
            }))

async def broadcast_clear(sender):
    # Clear drawing for all clients except the sender
    for client in clients:
        if client != sender:
            await client.send(json.dumps({
                'type': 'clear'
            }))

# Start WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()