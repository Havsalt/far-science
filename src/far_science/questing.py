from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from .dialogue import Message

if TYPE_CHECKING:
    from . import World


# NOTE: Will only trigger when in compartment the quest is attached to
class Quest:
    def __init__(
        self,
        start_condition: Callable[[World], bool] | None,  # Using lambdas
        start_message: Message | None,
        end_condition: Callable[[World], bool] | None = None,  # Using lambdas
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

    def can_start(self, world: World) -> bool:
        if self._start_condition is not None:
            return self._start_condition(world)
        return True  # Treat `None` as no condition, meaning instantly started

    def is_completed(self, world: World) -> bool:
        if self._end_condition is not None:
            return self._end_condition(world)
        return True  # Treat `None` as no condition, meaning instantly completed
