import asyncio
import websockets
import json
import random

# Store connected players and their game states
players = {}
games = {}

async def handle_connection(websocket, path):
    try:
        # Generate a unique player ID
        player_id = str(len(players) + 1)
        players[player_id] = {
            'websocket': websocket,
            'choice': None,
            'ready': False
        }

        # Notify the player of their ID
        await websocket.send(json.dumps({
            'type': 'player_id',
            'id': player_id
        }))

        await register_player(player_id, websocket)
    except Exception as e:
        print(f"Connection error: {e}")

async def register_player(player_id, websocket):
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            if data['type'] == 'make_choice':
                await handle_player_choice(player_id, data['choice'])
            elif data['type'] == 'ready':
                await mark_player_ready(player_id)
    except websockets.exceptions.ConnectionClosed:
        del players[player_id]

async def handle_player_choice(player_id, choice):
    players[player_id]['choice'] = choice
    
    # Check if we have two players ready to play
    ready_players = [p for p in players.values() if p['choice'] is not None]
    if len(ready_players) == 2:
        await resolve_game(ready_players)

async def mark_player_ready(player_id):
    players[player_id]['ready'] = True
    
    # Check if all players are ready to start
    if all(player['ready'] for player in players.values()):
        await broadcast_game_start()

async def resolve_game(ready_players):
    choices = [player['choice'] for player in ready_players]
    
    # Game logic
    results = {
        ('rock', 'scissors'): 0,
        ('scissors', 'paper'): 0,
        ('paper', 'rock'): 0
    }
    
    winner = None
    if choices[0] == choices[1]:
        result = 'Tie'
    elif (choices[0], choices[1]) in results:
        winner = 0
        result = 'Player 1 Wins!'
    elif (choices[1], choices[0]) in results:
        winner = 1
        result = 'Player 2 Wins!'
    
    # Broadcast results to all players
    for i, player in enumerate(ready_players):
        await player['websocket'].send(json.dumps({
            'type': 'game_result',
            'result': result,
            'winner': winner == i
        }))
    
    # Reset player states
    for player in players.values():
        player['choice'] = None
        player['ready'] = False

async def broadcast_game_start():
    for player in players.values():
        await player['websocket'].send(json.dumps({
            'type': 'game_start'
        }))

# Start WebSocket server
start_server = websockets.serve(handle_connection, "localhost", 8765)

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
