import pyglet

from pyglet.gl import GL_NEAREST
from pyglet.image import Texture

Texture.default_mag_filter = GL_NEAREST
Texture.default_min_filter = GL_NEAREST

class Renderer:
    def __init__(self, size):
        self.size = size

        self.window = pyglet.window.Window(1875, 96 * self.size, 'Hive')
        self.data = None

        @self.window.event
        def on_draw():
            self.window.clear()

            pyglet.shapes.Rectangle(
                0, 0, 1875, 96 * self.size,
                color=(18, 18, 18)
            ).draw()

            self.render()

    def run(self):
        pyglet.app.run()

    def load(self, data):
        self.data = data

    def render(self):
        if not self.data:
            return

        image = self.load_image('tiles/grass.png')

        for y in range(self.size):
            for x in range(self.size):
                self.draw_image(image, x, y)

        tiles = [
            (self.data.hives,   'hive'),
            (self.data.flowers, 'flower'),
            (self.data.walls,   'wall')
        ]

        for objs, tile in tiles:
            image = self.load_image(f'tiles/{tile}.png')

            for obj in objs:
                self.draw_image(image, obj['x'], obj['y'])

        for num, player in enumerate(self.data.players):
            image = self.load_image(f'bees/{num}.png')

            self.draw_image(image, player['x'], player['y'])

            sprite = pyglet.sprite.Sprite(
                image,
                x=1540,
                y=1090 - 10 - num * 250
            )
            sprite.scale = 45 / image.width
            sprite.draw()

        self.draw_label(
            f'Turn {self.data.game['turn']}',
            1540,
            1220,
            size=28,
            bold=True
        )

        for num, player in enumerate(self.data.players):
            off = num * 250
            highlight = player['id'] == 'self'

            self.draw_label(
                player['id'],
                1595,
                1090 - off,
                bold=True,
                highlight=highlight
            )

            self.draw_label(
                f'Pollen: {player['pollen']}',
                1545,
                1090 - 65 - off,
                highlight=highlight
            )

            hive = next(
                h for h in self.data.hives
                if h['player'] == player['id']
            )

            self.draw_label(
                f'Hive: {hive['pollen']}',
                1545,
                1090 - 120 - off,
                highlight=highlight
            )

    def load_image(self, path):
        image = pyglet.image.load(f'src/hive/tester/assets/{path}')

        image.anchor_x = 0
        image.anchor_y = 0

        return image

    def draw_image(self, image, x, y):
        x_pos = x * 96
        y_pos = y * 96

        sprite = pyglet.sprite.Sprite(
            image,
            x=x_pos,
            y=1440 - 96 - y_pos
        )
        sprite.scale = 96 / image.width

        sprite.draw()

    def draw_label(self, text, x, y, size=24, bold=False, highlight=False):
        pyglet.text.Label(
            text,
            x=x,
            y=y,
            font_name='Menlo',
            font_size=size,
            weight='bold' if bold or highlight else 'normal',
            color=(255, 210, 75) if highlight else (255, 255, 255)
        ).draw()
