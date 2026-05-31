import websockets
import json
import traceback

from .utils import load_map, TURNS

AUTH = '9fe2d786-82e4-4901-a969-9fe7af2d8988'

async def listen(id, game, move_fn):
    global path_map

    async with websockets.connect(f'wss://hive-api.ayukmr.com/play?auth={AUTH}&id={id}&game={game}') as ws:
        async for body in ws:
            data = json.loads(body)

            if data['type'] == 'next':
                data = data['data']

                load_map(data['walls'])

                for player in data['players']:
                    player['hive'] = [h for h in data['hives'] if h['player'] == player['id']][0]

                player = [p for p in data['players'] if p['id'] == id][0]

                out = 'stay'

                try:
                    out = move_fn(
                        {
                            'self': player,
                            'hive': player['hive'],

                            'game':    data['game'],
                            'players': data['players'],
                            'walls':   data['walls'],
                            'flowers': data['flowers'],
                            'hives':   data['hives']
                        }
                    )
                except Exception as e:
                    traceback.print_exception(e)

                print(f'> {out}')
                await send(ws, {'type': 'move', 'dir': out})

                if data['game']['turn'] == TURNS:
                    break
            elif data['type'] == 'error':
                raise RuntimeError(data['message'])

async def send(ws, data):
    await ws.send(json.dumps(data))
