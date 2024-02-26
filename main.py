import logging
import sys
from time import perf_counter, perf_counter_ns, sleep
from typing import Callable

from act import Act
from spotify import pause, playback, reset


def main():
    DELAY_MS = 0
    act = Act("HeatAboveGPT")
    act.start()

    print("")
    print(f"Playing Act {act.name}")
    print("")

    start_time_ms = None

    state = playback()
    while not state["is_playing"]:
        sleep(0.01)
        state = playback()

    start_time_ms = (perf_counter_ns() / 1e6) - state["progress_ms"]
    progress_ms = perf_counter_ns() / 1e6 - start_time_ms

    def update_progress():
        nonlocal progress_ms
        nonlocal start_time_ms
        progress_ms = (perf_counter_ns() / 1e6) - start_time_ms
        return progress_ms

    for time, sequence in act.progression.items():
        waited = False

        update_progress()
        while progress_ms + DELAY_MS < time * 1000:
            waited = True
            print(
                f"\r(next) sequence at {time}s (current: {round(progress_ms/1000, 2)}s)".ljust(
                    80
                ),
                end="",
            )

            sleep(0.001)
            update_progress()

        if waited:
            print("")

        start = perf_counter()
        sequence.exec(act)
        diff = perf_counter() - start
        print(
            f"exec took {round(diff, 1)}s -- off by {(progress_ms+DELAY_MS) - time}ms"
        )
        print("\n")

    print(f"Done! Last time {round(progress_ms/1000, 2)}s")
    pause()


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout, filemode="w", level=logging.INFO, format="%(message)s"
    )
    logger = logging.getLogger()

    reset()
    try:
        main()
    except KeyboardInterrupt:
        pause()
