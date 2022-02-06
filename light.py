import logging
from time import perf_counter, perf_counter_ns
from color import Color
from bridge import b


class Light:
    def __init__(self, name: str = None, smoo: int = 0):
        self.name = name
        self._smoo = smoo

    def _send(self, **kwargs):
        start = perf_counter_ns()
        for key, value in kwargs.items():
            # logging.debug(f"{self.name.ljust(25)} {key.upper().ljust(5)} {value}")
            b.set_light(self.name, key, value, transitiontime=self._smoo)
        # logging.debug(f"{self.name} took {(perf_counter_ns() - start)/1e6}ms")

    def on(self, bri: int = 0, color: Color = None):
        self._send(on=True, bri=0)
        self.color(color, bri=bri)

    def color(self, color: Color = None, bri: int = 255):
        if color is None:
            color = Color("#000000")
        self._send(bri=int(color.bri()), xy=color.xy())

    def off(self):
        self._send(on=False, bri=0)

    def smoo(self, smoo: int = 0):
        self._smoo = smoo
