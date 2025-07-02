import pyglet

from .runner import Runner

SIZE = 15

def run(move_fn, turns=20, size=15):
    tester = Runner(size, move_fn)

    pyglet.clock.schedule_interval(
        lambda _: tester.turn(turns), 1
    )

    tester.renderer.run()
