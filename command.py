from time import perf_counter, sleep
from typing import TYPE_CHECKING, Dict, List

from color import Color
from exceptions import TimecodeError
from light_modifier import Fade, Flash, Off, SetColor, Sparkle

if TYPE_CHECKING:
    from act import Act
    from light_modifier import AbstractLightModifier


class Command:
    def __init__(self, stages: List[str], modifier: "AbstractLightModifier"):
        self.stages = stages
        self.modifier = modifier
        self.description = f"{modifier.__class__.__name__} on {', '.join(stages)}"

    def exec(self, act: "Act"):
        for stage in self.stages:
            if stage not in act.stages:
                print(f"ERROR: stage not found: {stage}")
            act.stages[stage].apply(self.modifier)

    @classmethod
    def from_line(cls, line, color_map: Dict[str, Color] = None):
        line = line.replace("- ", "").strip()
        tokens = line.split(" ")

        stages = []
        colors = []
        durations = []
        command = None

        valid_commands = ["fade", "set", "dark", "flash", "sparkle"]

        for token in tokens:
            if token in valid_commands:
                command = token
            elif token.startswith("$"):
                stages.append(token)
            elif token.startswith("#"):
                if token not in color_map:
                    raise TimecodeError(
                        f"color {token} referenced but not defined: {line}"
                    )
                colors.append(color_map[token])
            elif token.endswith("s"):
                durations.append(float(token.strip("s")))

        if not stages:
            stages.append("$all")

        if command is None:
            raise TimecodeError(f"no command found: {line}")

        if command == "fade":
            if len(colors) == 0:
                raise TimecodeError(f"fade command requires a color: {line}")
            if len(durations) == 0:
                raise TimecodeError(f"fade command requires a duration: {line}")

            color = colors[0]
            duration = durations[0]
            modifier = Fade(color=color, duration_seconds=duration)

            return cls(
                stages=stages,
                modifier=modifier,
            )
        elif command == "dark":
            modifier = Off()
            return cls(
                stages=stages,
                modifier=modifier,
            )
        elif command == "set":
            if len(colors) == 0:
                raise TimecodeError(f"set command requires a color: {line}")

            color = colors[0]
            modifier = SetColor(color=color)
            return cls(
                stages=stages,
                modifier=modifier,
            )
        elif command == "flash":
            if len(colors) == 0:
                raise TimecodeError(f"flash command requires a color: {line}")
            if len(durations) == 0:
                raise TimecodeError(f"flash command requires a duration: {line}")

            color = colors[0]
            duration = durations[0]
            modifier = Flash(color=color, duration_seconds=duration)
            return cls(
                stages=stages,
                modifier=modifier,
            )
        elif command == "sparkle":
            if len(colors) == 0:
                raise TimecodeError(f"sparkle command requires a color: {line}")
            if len(durations) == 0:
                raise TimecodeError(f"sparkle command requires a duration: {line}")

            color = colors[0]
            duration = durations[0]
            modifier = Sparkle(color=color, duration_seconds=duration)
            return cls(
                stages=stages,
                modifier=modifier,
            )
        else:
            raise TimecodeError(f"invalid command: {command}")

    def __repr__(self) -> str:
        return self.description
