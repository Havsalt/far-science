from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest, instant as _instant

from ..station import CompartmentName as _CompartmentName


turn_on_heater: _Final = _Quest(
    _instant,
    [
        f"It's soOoOoO {_hint.wet('cold')} *fht* *fht*",
        ...,
        "The backup power isn't enough on its own",
        "to keep the heater working properly.",
        ...,
        f"I should find my way to the {_hint.info(_CompartmentName.NUCLEAR_REACTOR)}.",
        _hint.weak(
            "There might be some answers around, to what happened to this place..."
        ),
        ...,
        f"What will {_hint.weak('you')} do now?"
        + " " * 15
        + f"(type '{_hint.info('help')}' for list of actions)",
    ],
    lambda ctx: ctx.state.has_power,
    [
        "Somewhat warmer in here",
        ...,
        ...,
        "... for now at least",
    ],
)
inspect_tampering: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        f"There are signs of {_hint.clue('tampering')} with the {_hint.wet('cryo-pod')}.",
        ...,
        _hint.weak("Who could have done this?"),
        ...,
    ],
)
