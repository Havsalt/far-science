from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest


discover: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        "Let's just stay away from the equipment for now...",
        ...,
        ...,
        _hint.weak("please"),
    ],
)

search_for_the_crew: _Final = _Quest(
    lambda ctx: ctx.state.asked_ai_for_help
    and ctx.state.completed_initial_reports_for_ai,
    [
        "Well,",
        "there are nobody here...",
        ...,
        f"... and who even is this {_hint.bold('Snidri')}!",
        ...,
        ...,
        f"For all I know, {_hint.weak('"the crew"')} might not even be real,",
        _hint.weak("perhaps only imaginative friends?"),
        ...,
        "... but people of the imagination does certainly not",
        f"leave {_hint.clue('notes')} like {_hint.weak('these')} scattered around.",
    ],
)
