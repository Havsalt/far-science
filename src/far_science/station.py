from __future__ import annotations

import random
import itertools
from enum import StrEnum, auto
from dataclasses import dataclass, field
from typing import Literal

from . import bacteria
from .traits import HasName
from .questing import Quest
from .bool_state import Bool


type WordClass[T] = T
type IndefiniteArticle = Literal["a", "an"]


VOWELS = Literal[
    "a",
    "e",
    "i",
    "o",
    "u",
    "y",
]


class StationName(StrEnum):
    AKVARIS = auto()
    SOLARIS = auto()
    NEPRICON = auto()
    ATLAS = auto()

    def __str__(self) -> str:
        return super().__str__().replace("_", " ").title()


# This is just where is dump all shared quest states, regarding the station
@dataclass
class StationState:
    science: int = 0
    times_bonked_head: int = 0  # Accumulated from walking into walls
    has_power: bool = False
    asked_ai_for_help: bool = False
    completed_initial_reports_for_ai: Bool = Bool(False)
    inspected_soil: bool = False
    syringe: bacteria.Syringe | None = None
    has_picked_up_syringe: bool = False


@dataclass
class SpaceStation(HasName[StationName]):
    compartments: list[Compartment]
    state: StationState = field(default_factory=StationState)

    def __post_init__(self) -> None:
        # TODO: Make more fun space station structure
        # NOTE: Currently linear 1D space
        shuffled_compartments = self.compartments[:]
        random.shuffle(shuffled_compartments)
        for compartment, next_compartment in itertools.pairwise(shuffled_compartments):
            compartment.next_compartment = next_compartment
            next_compartment.prev_compartment = compartment


class CompartmentName(StrEnum):
    NUCLEAR_REACTOR = auto()
    SCIENCE_LAB = auto()
    MEDICAL_BAY = auto()
    SLEEP_POD = auto()
    CARGO = auto()
    AI_GUIDANCE_CENTER = auto()

    def __str__(self) -> str:
        return super().__str__().replace("_", " ").title()

    @property
    def article(self) -> WordClass[IndefiniteArticle]:
        if self.value[0].lower() in VOWELS.__args__:
            return "an"
        return "a"


class Compartment(HasName[CompartmentName]):
    def __init__(
        self,
        name: CompartmentName,
        *quests: Quest,
        quest_stage: int = 0,
        discovered: bool = False,
        condition: int = 100,  # From 0-100, where 0 is BROKEN state
        next_compartment: Compartment | None = None,
        prev_compartment: Compartment | None = None,
    ):
        self.name = name
        self.quests = quests
        self.quest_stage = quest_stage
        self.is_discovered = discovered
        self.condition = condition
        self.next_compartment = next_compartment
        self.prev_compartment = prev_compartment

    @property
    def current_quest(self) -> Quest:
        return self.quests[self.quest_stage]

    @property
    def quest_count(self) -> int:
        return len(self.quests)
