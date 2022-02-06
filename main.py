import logging
import sys
from time import perf_counter, perf_counter_ns, sleep
from turtle import update
from act import Act

from spotify import pause, playback, reset


def main():
    DELAY_MS = 150
    act = Act("EmoGirl")
    act.start()

    print(f"Playing Act -> {act.name} <-")

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

    for time, sequence in act.progression:
        time *= 100
        waited = False

        update_progress()
        while progress_ms + DELAY_MS < time:
            waited = True
            print(
                f"\r(next) {sequence} at {time/100} (current: {round(progress_ms/100, 2)})".ljust(
                    80
                ),
                end="",
            )

            sleep(0.001)
            update_progress()

        if waited:
            print("")

        start = perf_counter()
        act.play(sequence)
        diff = perf_counter() - start
        print(
            f"{round(diff, 1)}s -- {sequence} -- off by {(progress_ms+DELAY_MS) - time}ms"
        )
        print("\n")

    print(f"Done! Last time {round(progress_ms/100, 2)}s")
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
