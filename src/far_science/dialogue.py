import random
import time
import os
from collections.abc import Sequence
from types import EllipsisType


type TextLine = str | EllipsisType
type Message = Sequence[TextLine]
type Seconds = float


def pause(delta: Seconds, /) -> None:
    if not os.environ.get("FAR_SCIENCE_INSTANT_TEXT"):
        time.sleep(delta)


def print_message(
    message: TextLine | Message,
    *extra_message_segments: TextLine,
    step_delta: Seconds = 1.5,
) -> None:
    if isinstance(message, (str, EllipsisType)):
        full_message = (message, *extra_message_segments)
    else:
        full_message = (*message, *extra_message_segments)
    for index, line in enumerate(full_message, start=1):
        print(line if isinstance(line, str) else "")
        if index != len(full_message):
            pause(step_delta)


def blocked_message() -> tuple[str, ...]:
    if random.randint(0, 1):
        return ("Nowhere to go...",)
    elif random.randint(0, 3):
        return ("Dead end...",)
    else:
        return (
            "Can't go through walls...",
            "Sometimes I wish thou :=)",
        )


def get_input_segments() -> list[str]:
    # fmt: off
    return (
        input("Action: ")
        .strip()
        .replace("  ", " ")
        .replace("  ", " ")
        .lower()
        .split()
    )
    # fmt: on
