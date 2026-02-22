from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest


turn_on_main_power: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        "Still working.",
        "Should k#ep this running at all costs.",
    ],
    lambda ctx: ctx.state.has_power,
    [
        "*Pushed power button*",
        ...,
        f"{_hint.clue('Voice')}: Power, online",
    ],
)
