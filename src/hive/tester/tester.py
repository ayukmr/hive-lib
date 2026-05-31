from hive.utils import SECS, TURNS

from .runner import Runner

def run(move_fn, copy, headless):
    tester = Runner(move_fn, copy, headless)

    if not headless:
        import pyglet

        pyglet.clock.schedule_interval(
            lambda _: tester.turn(), SECS / TURNS
        )

        tester.renderer.run()
    else:
        for _ in range(TURNS):
            tester.turn()
