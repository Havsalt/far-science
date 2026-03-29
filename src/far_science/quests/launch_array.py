from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest


discover: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        "There are many buttons and launch pods here",
    ],
)

prepare_launch: _Final = _Quest(
    lambda ctx: ctx.state.planted_seeds,  # TODO: Change out with "got_formula"
    [
        "Now that I got the formula,",
        "I need to access the control panel to launch one of the pods.",
    ],
    lambda ctx: ctx.state.staged_launch,
)
