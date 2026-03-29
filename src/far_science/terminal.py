from enum import StrEnum as _StrEnum, unique as _unique
from collections import defaultdict as _defaultdict
from typing import Final as _Final

from . import hint as _hint
from .dialogue import (
    get_input_segments as _get_input_segments,
    print_message as _print_message,
)
from .context import (
    Context as _Context,
    Condition as _Condition,
    always as _always,
)


@_unique
class Username(_StrEnum):
    HOLTAN = "kholtan"
    DOLORIS = "dserrano"
    # TODO: Add "MINE" member, which is the one main quest expects
    #     - Have "HOLTAN" as optional extra lore, that is only available if read first


# NOTE: Not safe to use with `typing.assert_never`
@_unique
class Choice(_StrEnum):
    VIEW_COMMANDS = "compgen -c"
    CHANGE_USER_PROFILE = f"sudo -iu {Username.DOLORIS}"
    OPEN_MISSION_LOGS = "cat mission_logs.txt"
    LAUNCH_POD = "./launch_pod.sh"
    EXIT = "exit"

    @property
    def pretty_name(self) -> str:
        assert self.name is not None, "How was this `None`??"
        return self.name.replace("_", " ").capitalize()


CHOICE_CONDITIONS: _Final = _defaultdict[Choice, _Condition](
    lambda: _always,
    {
        Choice.CHANGE_USER_PROFILE: lambda ctx: ctx.state.terminal_user
        is not Username.DOLORIS
    },
)


def get_choice() -> Choice:
    prompt = "crw-" + Username.HOLTAN + "% "
    segments = _get_input_segments(prompt)
    member_value = " ".join(segments)

    while member_value not in Choice._value2member_map_:
        _print_message(_hint.invalid(f"fatal: {' '.join(segments)}: command not found"))
        segments = _get_input_segments(prompt)
        member_value = " ".join(segments)

    return Choice(member_value)


def read_mission_logs(ctx: _Context) -> None:
    # TODO: Add hacking to get into this + commander notes / "commanders eyes only"
    _print_message(
        _hint.label(f"== MISSION OF {ctx.station.name} =="),
        ...,
        "- Operate research facility",
        "> " + _hint.ok("ok"),
        f"- Develop plant-booster {_hint.bacteria('bactera')}",
        "> " + _hint.pending("in progress"),
        "- Extended testing on plants",
        "> " + _hint.bad("not started"),
        f"- Send the formula back to {_hint.label('homeworld')}",
        "> " + _hint.bad("not started"),
        ...,
        "This will aid in the war against hunger,",
        f"so the remaining {_hint.bold('3.2%')} of the population can rebuild.",
        ...,
        "SUCCEED BY ANY MEANS NECCESARY",
    )
