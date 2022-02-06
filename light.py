import json
import logging
from time import perf_counter, perf_counter_ns
from color import Color
from bridge import blitz


class Light:
    def __init__(self, name: str = None, smoo: int = 0):
        self.name = name
        self._smoo = smoo

    def _send(self, **kwargs):
        start = perf_counter_ns()
        blitz.set_light(
            self.name,
            transitiontime=self._smoo,
            **kwargs,
        )
        logging.info(f"{self.name.ljust(20)} {json.dumps(kwargs)}")
        logging.debug(f"{self.name} took {(perf_counter_ns() - start)/1e6}ms")

    def on(self, bri: int = 0, color: Color = None):
        self._send(on=True, bri=bri or int(color.bri()), xy=color.xy())

    def color(self, color: Color = None, bri: int = 255):
        self._send(on=True, bri=int(color.bri()), xy=color.xy())

    def off(self):
        self._send(on=False, bri=0)

    def smoo(self, smoo: int = 0):
        self._smoo = smoo
