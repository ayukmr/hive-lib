import asyncio

move_fn = None

def move(func):
    global move_fn

    if func.__code__.co_argcount != 1:
        raise TypeError(f'{func.__name__} must take exactly 1 argument')

    move_fn = func

    return func

def run(id=None):
    from . import socket

    if move_fn is None:
        raise RuntimeError('no function marked @hive.move')

    if not id:
        id = input('id: ')

    game = int(input('game: '))

    print('---')

    asyncio.run(socket.listen(id, game, move_fn))

def test(copy=False):
    from . import tester

    if move_fn is None:
        raise RuntimeError('no function marked @hive.move')

    tester.run(move_fn, copy)
