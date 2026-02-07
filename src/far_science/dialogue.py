import random
import time
from collections.abc import Sequence
from types import EllipsisType


type TextLine = str | EllipsisType
type Message = Sequence[TextLine]


def print_message(
    message: TextLine | Message,
    *extra_message_segments: TextLine,
    step_time: float = 1.5,
) -> None:
    if isinstance(message, (str, EllipsisType)):
        full_message = (message, *extra_message_segments)
    else:
        full_message = (*message, *extra_message_segments)
    for index, line in enumerate(full_message, start=1):
        print(line if isinstance(line, str) else "")
        if index != len(full_message):
            time.sleep(step_time)


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
