import random

from .noise import Noise
from ..utils import SIZE

class Init:
    def __init__(self):
        self.players = []
        self.hives   = []
        self.flowers = []
        self.walls   = []

        self.init_players()

        self.create_walls()
        self.create_flowers()

    def init_players(self):
        players = ['self', 'pollen', 'nectar', 'honey']
        random.shuffle(players)

        locs = [
            (3, 3),
            (SIZE - 1 - 3, 3),
            (3, SIZE - 1 - 3),
            (SIZE - 1 - 3, SIZE - 1 - 3)
        ]

        for num, p_id in enumerate(players):
            x, y = locs[num]

            self.players.append({
                'id': p_id,
                'num': num,
                'x': x,
                'y': y,
                'pollen': 0
            })

            self.hives.append({
                'player': p_id,
                'x': x,
                'y': y,
                'pollen': 0
            })

    def create_walls(self):
        noise = Noise()
        scale = 1.0 / SIZE

        for y in range(1, SIZE // 2):
            for x in range(1, SIZE // 2):
                sample = noise.sample(x * 4 * scale, y * 4 * scale)

                if sample <= 0.6 or self.taken(x, y):
                    continue

                fx = SIZE - x - 1
                fy = SIZE - y - 1

                self.walls.append({'x': x, 'y': y})
                self.walls.append({'x': fx, 'y': y})
                self.walls.append({'x': x, 'y': fy})
                self.walls.append({'x': fx, 'y': fy})

    def create_flowers(self):
        for _ in range(random.randint(3, 4)):
            x = random.randint(0, SIZE // 2 - 1)
            y = random.randint(0, SIZE // 2 - 1)

            while self.taken(x, y):
                x = random.randint(0, SIZE // 2 - 1)
                y = random.randint(0, SIZE // 2 - 1)

            fx = SIZE - x - 1
            fy = SIZE - y - 1

            self.flowers.append({'x': x, 'y': y, 'pollen': 0})
            self.flowers.append({'x': fx, 'y': y, 'pollen': 0})
            self.flowers.append({'x': x, 'y': fy, 'pollen': 0})
            self.flowers.append({'x': fx, 'y': fy, 'pollen': 0})

    def taken(self, x, y):
        check = lambda os: any(
            o for o in os
            if o['x'] == x and o['y'] == y
        )

        hive   = check(self.hives)
        flower = check(self.flowers)
        wall   = check(self.walls)

        return hive or flower or wall
