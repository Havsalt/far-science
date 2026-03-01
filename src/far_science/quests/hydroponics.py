from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest, instant as _instant


discover: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        "I like the smell of fresh plant life!",
        _hint.weak("... but this is nothing but withered grass..."),
        ...,
        f"The {_hint.info('local control panel')} might show me some useful information.",
    ],
    lambda ctx: ctx.state.checked_hydroponics_status,
    [
        ...,
        "There is a lot to do.",
        "Might be able to make happy plants, with some hard effort.",
    ],
    # IDEA: Can add post event to ask AI for seeds, from CARGO?
)

fetch_soil: _Final = _Quest(
    _instant,
    None,
    lambda ctx: ctx.state.fetched_soil,
    [
        _hint.weak("You empty your pockets of soil, into one of the plant spots."),
        "This new soil should do the trick!",
    ],
    post_event=lambda ctx: ctx.state.soil_quality_is_good.set(True),
)

reach_good_plant_conditions: _Final = _Quest(
    _instant,
    None,
    lambda ctx: ctx.state.plant_conditions_are_good,
    [
        "Nice, now I can grow plants.",
        "But the thing is,",
        _hint.weak("I have no") + _hint.clue(" seeds ") + _hint.weak("to plant..."),
    ],
    post_event=lambda ctx: ctx.state.ready_to_get_seeds.set(True),
)
