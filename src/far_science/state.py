from __future__ import annotations

from enum import Flag, auto
from dataclasses import dataclass

from . import bacteria
from .bool_state import Bool


class WaterLevel(Flag):
    DRY = auto()
    """No water."""

    MOISTURE = auto()
    """When sprinkler is just turned on."""

    DECENT = auto()
    """After 1 day."""

    PERFECT = auto()
    """Reached perfect state after 2 days - Kept at perfect levels going forward."""

    @property
    def is_good(self) -> bool:
        return self in WaterLevel.DECENT | WaterLevel.PERFECT

    @property
    def has_active_sprinkling(self) -> bool:
        return self is not WaterLevel.DRY

    @property
    def next_stage(self) -> WaterLevel:
        members = list(WaterLevel)
        if self is members[-1]:
            return self
        next_member = members[(members.index(self) + 1) % len(members)]
        return next_member

    @property
    def pretty_name(self) -> str:
        assert self.name is not None, "How was this `None`??"
        return self.name.replace("_", " ").lower()


# This is just where is dump all shared quest states, regarding the station
# NOTE: Many of the bools will remain toggled, as they are a one-shot event
@dataclass
class StationState:
    helped_discover_after_move: bool = False
    science: int = 0
    times_bonked_head: int = 0  # Accumulated from walking into walls
    has_power: bool = False
    asked_ai_for_help: bool = False
    completed_initial_reports_for_ai: Bool = Bool(False)
    inspected_cargo_soil: bool = False
    fetched_soil: bool = False
    syringe: bacteria.Syringe | None = None
    took_syringe: bool = False  # To prevent picking up more syringes after use
    learned_about_vaccine_prototype: bool = False
    checked_hydroponics_status: bool = False
    water_level: WaterLevel = WaterLevel.DRY
    soil_quality_is_good: Bool = Bool(False)
    ready_to_get_seeds: Bool = Bool(False)
    has_seeds: Bool = Bool(False)
    planted_seeds = False

    @property
    def plant_conditions_are_good(self) -> bool:
        return (
            self.has_power
            and bool(self.soil_quality_is_good)
            and self.water_level.is_good
        )
