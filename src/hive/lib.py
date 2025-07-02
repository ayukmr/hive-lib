import asyncio

from . import socket, tester

move_fn = None

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

    asyncio.run(socket.listen(id, game, move_fn))

def test():
    if move_fn is None:
        raise RuntimeError('no function marked @hive.move')

    tester.run(move_fn)
