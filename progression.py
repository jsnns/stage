from typing import List, Tuple

from exceptions import TimecodeError
from sequence import Sequence


class Progresion:
    def __init__(self, sequences: List[Sequence]) -> None:
        self.sequences = sequences

        self.validate()

    def next(self, playback_time_seconds: float) -> List[Sequence]:
        for sequence in self.sequences:
            if sequence.start_at_seconds < playback_time_seconds:
                return sequence

    def items(self) -> List[Tuple[float, Sequence]]:
        return [(sequence.start_at_seconds, sequence) for sequence in self.sequences]

    def validate(self):
        # check that a sequence can safely start at the right time assuming the previous sequence ends after sequence.duration_seconds
        current_time = 0
        for i, s in enumerate(self.items()):
            start_time, sequence = s
            if start_time < current_time:
                raise TimecodeError(
                    f"Sequence sequence #{i+1} starts before the previous sequence ends. This sequence starts at {start_time}s and the previous sequence ends at {current_time}s."
                )
            current_time = start_time + sequence.duration_seconds
