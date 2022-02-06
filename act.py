from collections import defaultdict
from time import perf_counter, sleep
from typing import Dict, List, Tuple
from color import Color
from light import Light

from sequence import Sequence
from spotify import play


class Act:
    def __init__(self, name: str = None):
        self.name = name

        # scene vars
        self.colors: Dict[str, Color] = dict()
        self.stages: Dict[str, Dict[str, Light]] = defaultdict(dict)
        self.pace = 4
        self.smoothing = 0
        self.sequences: Dict[str, Sequence] = dict()
        self.progression: List[Tuple[int, str]] = []

        self.type = "timed"  # timed or song
        self.song = None

        self.lines = self.get_lines()
        self.parse()

    def start(self):
        if "init" in self.sequences:
            self.play("init")
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
        included_lines = []
        in_sequence = None
        times = None
        repeat_count = None
        repeat_interval = None
        for line in self.lines:
            if line[:3] == "SEQ":
                items = line[3:].strip().split(" ")
                name = items[0]
                in_sequence = name.strip()
                times = []
                for item in items[1:]:
                    if "[" in item:
                        repeat_count = int(item[1:-2])
                    if "]" in item:
                        repeat_interval = int(item[:-3])

                for item in items:
                    if item.isdigit():
                        times.append(int(item))
                continue
            if in_sequence and "END" in line:
                repeat = 1
                if "r" in line:
                    repeat = int(line.split("r")[1])
                self.sequences[in_sequence] = Sequence(included_lines, repeat=repeat)

                if repeat_count and repeat_interval:
                    for time in times:
                        for i in range(repeat_count):
                            self.progression.append(
                                (time + i * repeat_interval, in_sequence)
                            )
                else:
                    for time in times:
                        self.progression.append((time, in_sequence))

                included_lines = []
                in_sequence = None
                repeat_interval = None
                repeat_count = None
                continue
            if in_sequence:
                included_lines.append(line)

    def parse_config(self):
        for line in self.lines:
            if line[:3] == "SEQ":
                return
            if line[:4] == "PACE":
                self.pace = int(line[4:])
            if line[:4] == "SMOO":
                self.smoothing = int(line[4:])
            if line[:4] == "SONG":
                self.type = "song"
                self.song = line[4:].strip()

    def parse_colors(self):
        for line in self.lines:
            if line[:3] == "SEQ":
                return
            if line[0] == "#":
                name, color = line[1:].split(" ")
                color = color.replace('"', "")
                self.colors[name] = Color(color)

    def parse_stages(self):
        for line in self.lines:
            if line[:3] == "SEQ":
                return
            if line[0] == "$":
                stage, *light = line[1:].split(" ")
                light_name = " ".join(light).replace('"', "")
                self.stages[stage][light_name] = Light(light_name, smoo=self.smoothing)

    def get_lines(self) -> str:
        with open(f"scenes/{self.name}.sg", "r") as f:
            return [self.clean_line(line) for line in f.read().splitlines() if line]

    def clean_line(self, line: str) -> str:
        if (
            "--" in line[1:]
        ):  # ignore comments if they don't start at the beginning of the line
            index = line.index("--")
            return line[:index]
        return line

    def __repr__(self) -> str:
        return f"""<Act: {self.name} smoo={self.smoothing} pace={self.pace}>

Colors:
{list(f"{k}={v}" for k, v in self.colors.items())}

Stages:
{list(f"{k}={v}" for k, v in self.stages.items())}

Sequences:
{list(f"{k}={len(v.lines)}" for k, v in self.sequences.items())}
"""
