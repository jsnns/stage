from typing import List

from command import (
    AllOff,
    Clear,
    FinishAndSkip,
    FinishSecond,
    Off,
    SetColor,
    SetColorAll,
    Smoo,
)


class Sequence:
    def __init__(self, lines: List[str], repeat: int = 1):
        self.lines = lines
        self.repeat = repeat

        self.parse()

    def parse(self):
        commands = []
        for line in self.lines:
            if line in [".", "..", "..."]:
                commands.append(FinishSecond(len(line)))
                continue
            if line[:3] == "...":
                seconds_to_skip = int(line[3:])
                commands.append(FinishAndSkip(seconds_to_skip))
                continue
            if line[:3] == "all":
                if "off" in line:
                    commands.append(AllOff())
                elif "#" in line:
                    commands.append(SetColorAll(line[5:]))
                continue
            if line.startswith("smoo"):
                commands.append(Smoo(int(line[4:].strip())))
                continue
            if line == "clear":
                commands.append(Clear())
                continue
            if line.startswith("off"):
                lights = line[3:].strip().split(" ")
                for light in lights:
                    commands.append(Off(light.replace("$", "")))
                continue

            command_parts = line.split(" | ")
            for part in command_parts:
                part = part.strip()
                if part.startswith("#"):
                    color, *lights = part[1:].split(" ")
                    for light in lights:
                        commands.append(SetColor(light.replace("$", ""), color))
                    continue
        print(commands)
        self.commands = commands * self.repeat
