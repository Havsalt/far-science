from dataclasses import dataclass

from . import bacteria
from .bool_state import Bool


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
    learned_about_vaccine_prototype: bool = False
