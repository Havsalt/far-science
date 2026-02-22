from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Final, final

from .traits import InsideStation, InsideCompartment
from .sentinel import Sentinel


type Percent = int
type NonNegative = int


VIRUS_GROWING_RATE: Final[Percent] = 5
SYRINGE_EFFECT: Final[NonNegative] = 21


@final
class VirusStage:
    @final
    class Dormant(metaclass=Sentinel): ...

    @final
    @dataclass(kw_only=True)
    class Growing:
        percent: int = 0


class Syringe(Enum):
    UNKNOWN_CONTENT = auto()
    KNOWN_VACCINE_PROTOTYPE = auto()


@dataclass
class Player(
    InsideStation,
    InsideCompartment,
):
    max_action_points: int
    action_points: int = field(init=False)
    virus_stage: type[VirusStage.Dormant] | VirusStage.Growing = VirusStage.Dormant

    def __post_init__(self) -> None:
        self.action_points = self.max_action_points
