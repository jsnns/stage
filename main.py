import logging
import sys
from time import perf_counter, sleep
from bridge import b
from act import Act

from spotify import pause, playback, reset


def main():
    DELAY_MS = 300
    act = Act("MGK-Tickets-Kiss_Kiss")
    act.start()

    print(f"Playing Act -> {act.name} <-")

    for time, sequence in act.progression:
        state = playback()
        time *= 100
        waited = False
        while (max(state["progress_ms"] + DELAY_MS, 0)) < time or not state[
            "is_playing"
        ]:
            waited = True
            print(
                f"\r(next) {sequence} at {time/100} (current: {state['progress_ms']/100})",
                end="",
            )
            if time - state["progress_ms"] > 1:
                sleep(0.25)
                state = playback()
                continue

            sleep(0.01)
            state = playback()

            if state["progress_ms"] == 0:
                main()
                break
        if waited:
            print("")
        start = perf_counter()
        actual_time = playback()["progress_ms"]
        act.play(sequence)
        diff = perf_counter() - start
        print(f"{round(diff, 1)}s -- {sequence} -- off by {actual_time - time}ms")

        if actual_time - time > 1000:
            pause()
            sleep(0.5)
            reset()
            exit()

        print("\n")

    pause()


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout, filemode="w", level=logging.INFO, format="%(message)s"
    )
    logger = logging.getLogger()

    b.connect()
    reset()
    try:
        main()
    except KeyboardInterrupt:
        pause()
