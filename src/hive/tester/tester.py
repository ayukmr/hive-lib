import pyglet

from hive.utils import TURNS

from .runner import Runner

def run(move_fn):
    tester = Runner(move_fn)

    pyglet.clock.schedule_interval(
        lambda _: tester.turn(), TURNS / 2000
    )

    tester.renderer.run()
