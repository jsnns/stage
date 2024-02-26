from typing import TYPE_CHECKING, Dict, List

from color import Color
from command import Command

if TYPE_CHECKING:
    from act import Act


class Sequence:
    def __init__(self, lines: List[str], colors: Dict[str, Color] = None):
        self.lines = lines
        self.start_at_seconds = 0
        self.commands: List[Command] = []

        self.parse(colors=colors)

    @property
    def duration_seconds(self):
        return max([command.modifier.duration_seconds for command in self.commands])

    def parse(self, colors: Dict[str, Color] = None):
        # get the start time
        for line in self.lines:
            if line.startswith("at"):
                # the line will look like 'at 10s'
                # we want to extract the number of seconds
                self.start_at_seconds = float(
                    line.replace("at", "").replace("s", "").strip()
                )
                break

        for line in self.lines:
            if line.startswith("-"):
                self.commands.append(Command.from_line(line, color_map=colors))

    def exec(self, act: "Act"):
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor() as executor:
            executor.map(lambda command: command.exec(act), self.commands)

    def queued(self):
        self.print_commands(prefix="⏳ ")

    def running(self):
        self.print_commands(prefix="🚦 ", clear=True)

    def completed(self):
        self.print_commands(prefix="✅ ", clear=True)

    def print_commands(self, prefix: str = "", clear: bool = False):
        commands = [f"{prefix}{command.description}" for command in self.commands]

        if clear:  # then we want to overwrite the previous output
            print("\033[F" * len(self.commands), end="")
            print("\033[K" * len(self.commands), end="")
        print("\n".join(commands))
