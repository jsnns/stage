from random import choice, random
from time import sleep
from typing import List, Tuple

from color import Color
from light import Light


class AbstractLightModifier:
    def modify(self, light: Light, index: int, total: int):
        raise NotImplementedError("Please Implement this method")

    @property
    def duration_seconds(self):
        return 0


class SetColor(AbstractLightModifier):
    def __init__(self, color: Color):
        self.color = color

    def modify(self, light: Light, index: int, total: int):
        light.smoo(0)
        light.on(color=self.color)


class Off(AbstractLightModifier):
    def modify(self, light: Light, index: int, total: int):
        light.off()


class Fade(AbstractLightModifier):
    def __init__(self, color: Color, duration_seconds: float):
        self.color = color
        self._duration_seconds = duration_seconds

    @property
    def duration_seconds(self):
        return self._duration_seconds

    def modify(self, light: Light, index: int, total: int):
        light.smoo(int(self.duration_seconds * 10))
        light.on(color=self.color)


class Flash(AbstractLightModifier):
    def __init__(self, color: Color, duration_seconds: float):
        self.color = color
        self._duration_seconds = duration_seconds

    @property
    def duration_seconds(self):
        return self._duration_seconds

    def modify(self, light: Light, index: int, total: int):
        on_time = 0.2
        off_time = 0.5

        total_time = self._duration_seconds
        while total_time > 0:
            light.smoo(0)
            light.on(color=self.color)
            sleep(on_time)
            light.smoo(0)
            light.off()
            sleep(off_time)
            total_time -= on_time + off_time


class Sparkle(AbstractLightModifier):
    def __init__(self, color: Color, duration_seconds: float):
        self.color = color
        self._duration_seconds = duration_seconds

    @property
    def duration_seconds(self):
        return self._duration_seconds

    def modify(self, light: Light, index: int, total: int):
        # a tuple of [time, brightness]
        transitions: List[Tuple[float, float]] = []
        total_time = self._duration_seconds

        # get random initial delay between 0 and 10% of the total time
        transitions.append((0, 0))  # start dark at 0

        while total_time > 0:
            # after delay turn on random brightness
            min_delay = self.duration_seconds * 0.05
            max_delay = self.duration_seconds * 0.2
            delay = random() * (max_delay - min_delay) + min_delay
            delay = min(delay, total_time)

            max_brightness = 1
            min_brightness = 0.5
            brightness = random() * (max_brightness - min_brightness) + min_brightness

            transitions.append((delay, brightness))
            total_time -= delay + 0.1

        for i, (time, brightness) in enumerate(transitions):
            # set smoo to be the time until the next transition
            if i == len(transitions) - 1:
                light.smoo(0)
            else:
                next_time = transitions[i + 1][0]
                light.smoo(int((next_time - time) * 10))

            light.on(color=self.color, bri=int(brightness * 255))
            sleep(time)
