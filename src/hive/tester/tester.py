import pyglet

from hive.utils import SECS, TURNS

from .runner import Runner

def run(move_fn, copy):
    tester = Runner(move_fn, copy)

    pyglet.clock.schedule_interval(
        lambda _: tester.turn(), SECS / TURNS
    )

    tester.renderer.run()
