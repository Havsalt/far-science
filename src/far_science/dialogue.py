import time
import os
from collections.abc import Sequence
from types import EllipsisType
from typing import Final


type Seconds = float
type TextLine = str | EllipsisType
type Message = Sequence[TextLine]
type Reason = TextLine | Message | None
type ActionNameSegments = list[str]


TEXT_LINE_TYPES: Final = (str, EllipsisType)


def pause(delta: Seconds, /) -> None:
    if not os.environ.get("FAR_SCIENCE_INSTANT_TEXT"):
        time.sleep(delta)


def print_message(
    message: TextLine | Message,
    *extra_message_segments: TextLine,
    step_delta: Seconds = 1.5,
) -> None:
    if isinstance(message, TEXT_LINE_TYPES):
        full_message = (message, *extra_message_segments)
    else:
        full_message = (*message, *extra_message_segments)
    for index, line in enumerate(full_message, start=1):
        print(line if isinstance(line, str) else "")
        if index != len(full_message):
            pause(step_delta)


def get_input_segments() -> ActionNameSegments:  # NOTE: Might not match
    # fmt: off
    return (
        input("Action: ")
        .strip()
        .replace("  ", " ")
        .replace("  ", " ")  # Perform twice to actually remove *all* double whitespace
        .lower()
        .split()
    )
    # fmt: on
