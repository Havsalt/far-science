from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest


discover_cargo: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        f"Can't seem to remember why we had so much {_hint.clue('soil')} with us.",
        "Were we gonna terraform Marz or something?",
    ],
)
