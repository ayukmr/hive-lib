import pyglet

from hive.utils import SECS, TURNS

from .runner import Runner

def run(move_fn):
    tester = Runner(move_fn)

    pyglet.clock.schedule_interval(
        lambda _: tester.turn(), SECS / TURNS
    )

    tester.renderer.run()
