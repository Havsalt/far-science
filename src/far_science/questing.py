from __future__ import annotations

from typing import Callable

from .dialogue import Message
from .context import Context

type Condition = Callable[[Context], bool]


# NOTE: Will only trigger when in compartment the quest is attached to
class Quest:
    def __init__(
        self,
        start_condition: Condition | None,  # Using lambda
        start_message: Message | None,
        end_condition: Condition | None = None,  # Using lambda
        end_message: Message | None = None,
        /,
    ) -> None:
        self._start_condition = start_condition  # Use as method-like
        self._end_condition = end_condition
        self.start_message = start_message
        self.end_message = end_message
        self.is_active = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.is_active=}, {self.start_message}, {self.end_message})"

    def can_start(self, ctx: Context) -> bool:
        if self._start_condition is not None:
            return self._start_condition(ctx)
        return True  # Treat `None` as no condition, meaning instantly started

    def is_completed(self, ctx: Context) -> bool:
        if self._end_condition is not None:
            return self._end_condition(ctx)
        return True  # Treat `None` as no condition, meaning instantly completed
