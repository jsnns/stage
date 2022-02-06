from time import sleep
import typing

from color import Color

if typing.TYPE_CHECKING:
    from act import Act


class Command:
    def __init__(self):
        self.type = None

    def __repr__(self):
        a = [
            f"{key}={value}"
            for key, value in list(self.__dict__.items())
            if key != "type"
        ]
        return f"<Command {self.type} {' '.join(a)}>"

    def exec(self, act: "Act"):
        raise NotImplementedError()


class SetColor(Command):
    def __init__(self, name, color):
        self.type = "set_color"
        self.name = name
        self.color = color

    def exec(self, act: "Act"):
        for light in act.stages[self.name].values():
            light.color(act.colors[self.color])


class Off(Command):
    def __init__(self, name):
        self.type = "off"
        self.name = name

    def exec(self, act: "Act"):
        for light in act.stages[self.name].values():
            light.off()


class FinishSecond(Command):
    def __init__(self, dots=1):
        self.type = "finish_second"
        self.dots = dots

    def exec(self, act: "Act"):
        sleep(self.dots / 4)


class FinishAndSkip(Command):
    def __init__(self, skip_seconds):
        self.type = "finish_and_skip"
        self.skip_seconds = int(skip_seconds) or 0

    def exec(self, act: "Act"):
        sleep(self.skip_seconds)


class AllOff(Command):
    def __init__(self):
        self.type = "all_off"

    def exec(self, act: "Act"):
        for stage in act.stages.values():
            for light in stage.values():
                light.off()


class Clear(Command):
    def __init__(self):
        self.type = "all_on"

    def exec(self, act: "Act"):
        for stage in act.stages.values():
            for light in stage.values():
                light.on(color=Color("#111111"), bri=1)


class SetColorAll(Command):
    def __init__(self, color):
        self.type = "set_color_all"
        self.color = color

    def exec(self, act: "Act"):
        for stage in act.stages.values():
            for light in stage.values():
                light.color(color=act.colors[self.color])


class Smoo(Command):
    def __init__(self, smoo: int = 0):
        self.type = "smoo"
        self.smoo = smoo

    def exec(self, act: "Act"):
        for stage in act.stages.values():
            for light in stage.values():
                light.smoo(self.smoo)
