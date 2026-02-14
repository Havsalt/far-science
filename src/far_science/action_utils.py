from __future__ import annotations

from functools import wraps
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Generator, Literal, Final, final, override

from .station import CompartmentName
from .context import Context

if TYPE_CHECKING:
    from .world_gen import World

type ActionClassName = str
type ActionNameSegments = list[str]
# Individual actions are defined as public methods
type Action = Callable[[Context], None]
type Condition = Callable[[Context], bool]
type Place = CompartmentName | type[anywhere]


@dataclass
class ConditionalAction:
    fn: Action
    condition: Condition
    trigger: ActionNameSegments
    desc: str


# Public export
all_actions: Final = dict[Place, dict[str, ConditionalAction]]()


class Sentinel(type):
    __new__: None = None

    def __repr__(cls) -> str:
        return f"<{__class__.__name__}(<{cls.__name__}>)>"


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
    alias: list[str] | None = None,
):
    def decorator(fn: Action):
        if where not in all_actions:
            all_actions[where] = {}
        if alias is not None:
            action_name_segments = alias
        else:
            action_name_segments = fn.__name__.split("_")

        if description is not None:
            final_desc = description
        else:
            final_desc = fn.__name__.replace("_", " ").capitalize()

        all_actions[where][fn.__name__] = ConditionalAction(
            fn,
            when,
            action_name_segments,
            final_desc,
        )

        @wraps(fn)
        def wrapper(ctx: Context) -> None:
            fn(ctx)

        return wrapper

    return decorator


def get_available_actions(
    world: World,
) -> Generator[ConditionalAction, None, None]:
    compartment = world.player.compartment
    place_actions = all_actions.get(compartment.name, dict())
    anywhere_actions = all_actions.get(anywhere, dict())
    possible_actions = place_actions | anywhere_actions
    ctx = Context(world)
    for action in possible_actions.values():
        if action.condition(ctx):
            yield action
