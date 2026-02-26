from typing import Final as _Final

from .. import hint as _hint
from ..questing import Quest as _Quest

from ..action_utils import CompartmentName as _CompartmentName


discover: _Final = _Quest(
    lambda ctx: ctx.compartment.is_discovered,
    [
        f"I {_hint.weak("don't")} feel alone in here...",
        ...,
        ...,
        f"{_hint.weak('Still')} not alone...",
        ...,
    ],
)

encounter_ai: _Final = _Quest(
    lambda ctx: ctx.state.has_power,
    [
        f"{_hint.clue('Voice')}: Hello there... *bzZt*",
        ...,
        f"You have been gone for {_hint.clue('-27429999...')}"
        + f" {_hint.error('ERROR: Malformed number')}",
        ...,
        _hint.weak("Me: *hmm*"),
        _hint.weak("    A working AI on the station?"),
        ...,
    ],
)

complete_initial_reports: _Final = _Quest(
    lambda ctx: ctx.state.asked_ai_for_help,
    [
        "AI: You got work to do,",
        f"    which seems to be aproxim#tly {_hint.info('5 science')} reports",
    ],
    lambda ctx: ctx.state.science >= 5,
    [
        "AI: Acceptable work.",
        ...,
        f"AI: Unlike the rest of the {_hint.clue('crew')}...",
        f"    They have been little productive for the last {_hint.error('<BAD TIMESPAN>')}",
        ...,
        "Me: Crew?",
        ...,
        "AI: There is a lot of work to catch up with,",
        "    since nobody else is as capable as you in the lab.",
        ...,
        ...,
        f"AI: Check if {_hint.clue('Snidri')} is done with his {_hint.bacteria('project')}"
        + f" in the {_hint.label(_CompartmentName.MEDICAL_BAY)}.",
        "    He is long over schedule... *bzZt*",
    ],
    post_event=lambda ctx: ctx.state.completed_initial_reports_for_ai.set(True),
)
