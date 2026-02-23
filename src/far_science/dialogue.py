from __future__ import annotations

import random
import string
import time
import os
from collections.abc import Sequence
from types import EllipsisType
from typing import Final

from . import bacteria
from .context import Context


type Seconds = float
type Percent = int
type TextLine = str | EllipsisType
type Message = Sequence[TextLine]
type Reason = TextLine | Message | None
type ActionNameSegments = list[str]


TEXT_LINE_TYPES: Final = (str, EllipsisType)


def pause(delta: Seconds, /) -> None:
    if not os.environ.get("FAR_SCIENCE_INSTANT_TEXT"):
        time.sleep(delta)


def scramble_fn(x: int) -> float:
    # return -0.000125 * x ** 2 + 0.0525 * x
    # TODO: Use the commented formula,
    #       once handling of "owned speach lines" has been implemented,
    #       and colors are escaped
    return 0


def scramble_speach(text: str, percent: Percent) -> str:
    adjusted_percent = scramble_fn(percent)
    result = ""
    for char in text:
        if random.randint(1, 100) > adjusted_percent:
            result += char
        else:
            result += random.choice(string.punctuation)
    return result


def print_message(
    message: TextLine | Message,
    *extra_message_segments: TextLine,
    step_delta: Seconds = 1.5,
) -> None:
    from .world_gen import world  # Lazy import

    ctx = Context(world)

    scramble_percent = 0
    if isinstance(ctx.player.bacteria_stage, bacteria.Stage.Growing):
        scramble_percent = ctx.player.bacteria_stage.percent

    if isinstance(message, TEXT_LINE_TYPES):
        full_message = (message, *extra_message_segments)
    else:
        full_message = (*message, *extra_message_segments)

    for index, line in enumerate(full_message, start=1):
        text = line if isinstance(line, str) else ""
        print(scramble_speach(text, percent=scramble_percent))

        if index != len(full_message):
            pause(step_delta)


def get_input_segments() -> ActionNameSegments:  # NOTE: Might not match
    return (
        input("Action: ")
        .strip()
        .replace("  ", " ")
        .replace("  ", " ")  # Perform twice to actually remove *all* double whitespace
        .lower()
        .split()
    )
