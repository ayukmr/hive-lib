import random

from .noise import Noise

class Init:
    def __init__(self, size):
        self.size = size

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
            (self.size - 1 - 3, 3),
            (3, self.size - 1 - 3),
            (self.size - 1 - 3, self.size - 1 - 3)
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
        scale = 1.0 / self.size

        for y in range(2, self.size - 2):
            for x in range(2, self.size - 2):
                sample = noise.sample(x * 4 * scale, y * 4 * scale)

                if sample <= 0.7 or self.taken(x, y):
                    continue

                self.walls.append({ 'x': x, 'y': y })

    def create_flowers(self):
        for _ in range(random.randint(10, 15)):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            while self.taken(x, y):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)

            self.flowers.append({
                'x': x,
                'y': y,
                'pollen': 0
            })

    def taken(self, x, y):
        check = lambda os: any(
            o for o in os
            if o['x'] == x and o['y'] == y
        )

        hive   = check(self.hives)
        flower = check(self.flowers)
        wall   = check(self.walls)

        return hive or flower or wall
