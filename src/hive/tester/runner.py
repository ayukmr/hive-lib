import random

from .init import Init
from .renderer import Renderer

from ..utils import towards, load_map

class Runner:
    def __init__(self, size, move_fn):
        self.size = size
        self.move_fn = move_fn

        self.renderer = Renderer(size)

        self.game = {
            'id': 1,
            'turn': 1
        }

        init = Init(size)

        self.players = init.players
        self.hives   = init.hives
        self.flowers = init.flowers
        self.walls   = init.walls

        load_map(self.walls)

    def turn(self, turns):
        if self.game['turn'] >= turns:
            return

        data = self.data()

        for player in self.players:
            id = player['id']

            plyr = [p for p in data['players'] if p['id'] == id][0]
            hive = [h for h in data['hives'] if h['player'] == id][0]

            local = data | {
                'self': plyr,
                'hive': hive
            }

            if id == 'self':
                out = self.move_fn(local)
                print(f'> {out}')
            else:
                out = self.bot(local)

            self.move(player, out)

        self.finish_turn()

    def bot(self, data):
        return random.choice(['stay', 'left', 'right', 'down', 'up'])

    def move(self, player, dir):
        dirs = {
            'stay':  ( 0,  0),
            'left':  (-1,  0),
            'right': ( 1,  0),
            'up':    ( 0, -1),
            'down':  ( 0,  1)
        }

        ds = dirs.get(dir)

        if not ds:
            print(f'error: invalid direction `{dir}`')
            return

        dx, dy = ds

        x = player['x'] + dx
        y = player['y'] + dy

        if not 0 <= x < self.size or not 0 <= y < self.size:
            return

        blocked = any(
            w for w in self.walls
            if w['x'] == x and w['y'] == y
        )

        if not blocked:
            player['x'] = x
            player['y'] = y

    def finish_turn(self):
        self.handle_flowers()
        self.handle_collisions()
        self.handle_hives()

        self.game['turn'] += 1

        self.renderer.load(self)

    def handle_flowers(self):
        for flower in self.flowers:
            flower['pollen'] += 1

        for player in self.players:
            x = player['x']
            y = player['y']

            flower = next(
                (
                    f for f in self.flowers
                    if f['x'] == x and f['y'] == y
                ),
                None
            )

            if not flower:
                continue

            player['pollen'] += flower['pollen']
            flower['pollen'] = 0

    def handle_collisions(self):
        pos = set((p['x'], p['y']) for p in self.players)

        for x, y in pos:
            players = [
                p for p in self.players
                if p['x'] == x and p['y'] == y
            ]

            hive = next(
                (
                    h for h in self.hives
                    if h['x'] == x and h['y'] == y
                ),
                None
            )

            if len(players) < 2 or not hive:
                continue

            for player in players:
                for other in players:
                    if player['num'] >= other['num']:
                        continue

                    h_player = hive['player']

                    if h_player == player['id']:
                        self.give_reset(other, player)
                    elif h_player == other['id']:
                        self.give_reset(player, other)

        pos = set((p['x'], p['y']) for p in self.players)

        for x, y in pos:
            players = [
                p for p in self.players
                if p['x'] == x and p['y'] == y
            ]

            pollens = [p['pollen'] for p in players]
            avg = int(sum(pollens) / len(pollens))

            for player in players:
                player['pollen'] = avg

    def give_reset(self, src, dest):
        dest['pollen'] += src['pollen']

        hive = next(
            h for h in self.hives
            if h['player'] == src['id']
        )

        src['x'] = hive['x']
        src['y'] = hive['y']
        src['pollen'] = 0

    def handle_hives(self):
        for player in self.players:
            x = player['x']
            y = player['y']

            hive = next(
                (
                    h for h in self.hives
                    if h['x'] == x and h['y'] == y
                ),
                None
            )

            if not hive:
                continue

            p_id = player['id']
            p_pollen = player['pollen']

            h_player = hive['player']
            h_pollen = hive['pollen']

            h_delta = 1 if p_id == h_player else -1

            if (h_delta == 1 and p_pollen == 0) or (h_delta == -1 and h_pollen == 0):
                continue

            player['pollen'] = p_pollen + -h_delta
            hive['pollen'] = h_pollen + h_delta

    def data(self):
        return {
            'game':    self.game,
            'players': self.players,
            'hives':   self.hives,
            'flowers': self.flowers,
            'walls':   self.walls
        }
