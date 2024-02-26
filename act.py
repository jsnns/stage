from collections import defaultdict
from time import perf_counter, sleep
from typing import Dict, List, Tuple

from color import Color
from light import Light, Stage
from light_modifier import Off
from progression import Progresion
from sequence import Sequence
from spotify import play

DEFAULT_COLORS = {
    "#dark": Color("#000001"),
    "#white": Color("#ffffff"),
}


class Act:
    def __init__(self, name: str = None):
        self.name = name
        self.colors: Dict[str, Color] = DEFAULT_COLORS
        self.stages: Dict[str, Stage] = defaultdict(Stage)
        self.sequences: List[Sequence] = []
        self.lights: List[Light] = []
        self.song = None

        self.lines = self.get_lines()
        self.parse()

    @property
    def progression(self) -> Progresion:
        return Progresion(self.sequences)

    def start(self):
        self.stages["$all"].apply(Off())

        sleep(3)
        play(song=self.song)

    def play(self, name):
        for command in self.sequences[name].commands:
            command.exec(self)

    def parse(self):
        # setup
        self.parse_config()
        self.parse_colors()
        self.parse_stages()

        # sequences
        self.parse_sequences()

    def parse_sequences(self):
        # a sequence starts with 'at Xs' which is the time in deciseconds to
        # start the sequence. it is followed by a list of commands to execute
        # in parallel. each command is on a new line and starts with '-'.
        # a sequence ends with a blank line or the end of the file.

        sequences: List[List[str]] = []

        new_sequence = None
        for line in self.lines:
            if line.startswith("at"):
                if new_sequence:
                    sequences.append(new_sequence)
                    new_sequence = []
                new_sequence = [line]
            elif line.startswith("-"):
                new_sequence.append(line)
            elif new_sequence:
                new_sequence.append(line)
                new_sequence = None
        if new_sequence:
            sequences.append(new_sequence)

        for sequence in sequences:
            self.sequences.append(Sequence(sequence, colors=self.colors))

    def parse_config(self):
        for line in self.lines:
            if line.startswith("SONG"):
                self.type = "song"
                self.song = line.strip("SONG").strip()

    def parse_colors(self):
        for line in self.lines:
            if line.startswith("#"):
                name, color = line.split(" ")
                color = color.replace('"', "")
                self.colors[name] = Color(color)

    def parse_stages(self):
        for line in self.lines:
            if line.startswith("$"):
                stage, *light = line.split(" ")
                light_name = " ".join(light).replace('"', "")
                self.stages[stage].add(Light(light_name))
                self.lights.append(Light(light_name))

        # add default stages
        self.stages["$all"] = Stage()
        for light in self.lights:
            self.stages["$all"].add(light)

    def get_lines(self) -> str:
        with open(f"scenes/{self.name}.timecode", "r") as f:
            return [self.clean_line(line) for line in f.read().splitlines() if line]

    def clean_line(self, line: str) -> str:
        if (
            "--" in line[1:]
        ):  # ignore comments if they don't start at the beginning of the line
            index = line.index("--")
            return line[:index]
        if "// " in line[1:]:
            index = line.index("// ")
            return line[:index]
        return line.strip()

    def __repr__(self) -> str:
        return f"""<Act: {self.name}>

Colors:
{list(f"{k}={v}" for k, v in self.colors.items())}

Stages:
{list(f"{k}={v}" for k, v in self.stages.items())}

Sequences:
{list(f"{s}" for s in self.sequences)}
"""
