# Namespace module

from . import (
    ai_guidance_center as ai_guidance_center,
    cargo_hold as cargo_hold,
    medical_bay as medical_bay,
    nuclear_reactor as nuclear_reactor,
    science_lab as science_lab,
    sleep_pod as sleep_pod,
)


# DEV: Remove this when reaching major version 1
from typing import Final
from .. import hint as _hint
from ..questing import Quest as _Quest
from ..action_utils import always as _instant

to_be_continued: Final = _Quest(
    _instant,
    [
        _hint.label("== TO BE CONTINUED =="),
        ...,
        f"You have {_hint.info('completed all the main quests')}, {_hint.weak('for now')}.",
        f"There might still be some objects to {_hint.info("inspect")},",
        f"{_hint.info("rooms")} to discover,",
        f"or {_hint.info("notes")} to read.",
        ...,
        f"Hope you liked the {_hint.info('story')} so far.",
        f"The goal is to {_hint.bold('expand it in the future')}.",
        ...,
        _hint.label("== THANKS FOR PLAYING =="),
    ],
)
