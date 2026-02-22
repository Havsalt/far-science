from __future__ import annotations

from functools import wraps
from dataclasses import dataclass
from typing import Callable, Generator, Literal, Final, final

from .station import CompartmentName
from .context import Context
from .sentinel import Sentinel
from .dialogue import TextLine, Message, ActionNameSegments

type ActionClassName = str
# Individual actions are defined as public methods
type Action = Callable[[Context], None]
type UnavailableAction = Callable[[Context], Reason]
type Reason = TextLine | Message | None
type SkipAction = Callable[[Context], None]  # TODO: Implement
type Condition = Callable[[Context], bool]
type Place = type[anywhere] | CompartmentName


@dataclass
class ConditionalAction:
    perform: Action
    condition_met: Condition
    name_segments: ActionNameSegments
    description: str
    when_unavailable: UnavailableAction | None = None
    skip_if: Condition | None = None


all_compartment_actions: Final = dict[Place, dict[str, ConditionalAction]]()
"""**Public export**.

Contains all available actions, associated with each compartment.
"""


@final
class anywhere(metaclass=Sentinel): ...


def always(_: Context) -> Literal[True]:
    return True


def action(
    where: Place,
    when: Condition,
    /,
    description: str | None = None,
    *,
    when_unavailable: UnavailableAction | None = None,
    skip_if: Condition | None = None,
    alias: list[str] | None = None,
):
    def decorator(fn: Action):
        if where not in all_compartment_actions:
            all_compartment_actions[where] = {}
        if alias is not None:
            action_name_segments = alias
        else:
            action_name_segments = fn.__name__.split("_")

        if description is not None:
            final_description = description
        else:
            final_description = fn.__name__.replace("_", " ").capitalize()

        all_compartment_actions[where][fn.__name__] = ConditionalAction(
            perform=fn,
            condition_met=when,
            name_segments=action_name_segments,
            description=final_description,
            skip_if=skip_if,
            when_unavailable=when_unavailable,
        )

        @wraps(fn)
        def wrapper(ctx: Context) -> None:
            fn(ctx)

        return wrapper

    return decorator


def get_action_by_name(
    name_segments: ActionNameSegments,
    /,
) -> ConditionalAction | None:
    for action in get_all_actions():
        if name_segments == action.name_segments:
            return action
    return None


def get_all_actions() -> Generator[ConditionalAction, None, None]:
    for compartment_actions in all_compartment_actions.values():
        for action in compartment_actions.values():
            yield action


def get_available_actions(
    ctx: Context,
) -> Generator[ConditionalAction, None, None]:
    compartment_actions = all_compartment_actions.get(ctx.compartment.name, dict())
    anywhere_actions = all_compartment_actions.get(anywhere, dict())
    possible_actions = compartment_actions | anywhere_actions
    for action in possible_actions.values():
        if action.condition_met(ctx):
            yield action
