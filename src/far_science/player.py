from dataclasses import dataclass, field
from typing import Final

from . import bacteria
from .traits import InsideStation, InsideCompartment


type Percent = int
type NonNegative = int


BONKS_UNTIL_HEAD_TRAUMA: Final[NonNegative] = 3


@dataclass
class Player(
    InsideStation,
    InsideCompartment,
):
    max_action_points: int
    action_points: int = field(init=False)
    virus_stage: type[bacteria.Stage.Dormant] | bacteria.Stage.Growing = (
        bacteria.Stage.Dormant
    )

    def __post_init__(self) -> None:
        self.action_points = self.max_action_points
