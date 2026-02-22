from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest


discover: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        "Used to be caught up in some report or project.",
        "It was fun while it last~d...",
        ...,
        _hint.weak("Really miss doing some") + " " + _hint.info("science") + "...",
        ...,
    ],
)
