import asyncio
import websockets

import json

AUTH = '9fe2d786-82e4-4901-a969-9fe7af2d8988'

move_fn = None
path_map = None

def move(func):
    global move_fn

    if move_fn is not None:
        raise RuntimeError('only one function can be marked @hive.move')

    if func.__code__.co_argcount != 1:
        raise TypeError(f'{func.__name__} must take exactly 1 argument')

    move_fn = func

    return func

def run():
    if move_fn is None:
        raise RuntimeError('no function marked @hive.move')

    id = input('id: ')
    game = int(input('game: '))

    print('---')

    asyncio.run(listen(id, game))

async def listen(id, game):
    global path_map

    async with websockets.connect(
        f'wss://hive-api.ayukmr.com/play?auth={AUTH}&id={id}&game={game}'
    ) as ws:
        async for body in ws:
            data = json.loads(body)

            if data['type'] == 'next':
                data = data['data']

                if path_map is None:
                    path_map = [[1 for _ in range(15)] for _ in range(15)]

                    for wall in data['walls']:
                        x, y = wall['x'], wall['y']
                        path_map[y][x] = 0

                player = [p for p in data['players'] if p['id'] == id][0]
                hive = [h for h in data['hives'] if h['player'] == id][0]

                out = move_fn(
                    {
                        'self': player,
                        'hive': hive,

                        'game':    data['game'],
                        'players': data['players'],
                        'walls':   data['walls'],
                        'flowers': data['flowers'],
                        'hives':   data['hives']
                    }
                )

                print(f'> {out}')

                await send(ws, { 'type': 'move', 'dir': out })

                if data['game']['turn'] == 20:
                    break
            elif data['type'] == 'error':
                raise RuntimeError(data['message'])

async def send(ws, data):
    await ws.send(json.dumps(data))

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

def towards(pos, dest):
    grid = Grid(matrix=path_map)

    p_x, p_y = pos
    d_x, d_y = dest

    start = grid.node(p_x, p_y)
    end = grid.node(d_x, d_y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)

    step = path[1] if len(path) > 1 else None

    if step:
        delta = (step.x - p_x, step.y - p_y)

        dirs = {
            (-1,  0): 'left',
            ( 1,  0): 'right',
            ( 0, -1): 'up',
            ( 0,  1): 'down'
        }

        return dirs[delta]
    else:
        return 'stay'
