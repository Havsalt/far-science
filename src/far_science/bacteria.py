from dataclasses import dataclass
from enum import Enum, auto
from typing import Final, final

from .sentinel import Sentinel


type Percent = int
type NonNegative = int


DAYS_UNTIL_DEATH: Final[NonNegative] = 9
"""A rough estimate on how long it takes for the bacteria to kill"""

VIRUS_GROWING_RATE: Final[Percent] = 100 // DAYS_UNTIL_DEATH
SYRINGE_EFFECT: Final[NonNegative] = 21


@final
class VirusStage:
    """Tagged union.

    Variants:
        - `type[Dormant]`
        - `Growing`
    """

    @final
    class Dormant(metaclass=Sentinel): ...

    @final
    @dataclass(kw_only=True)
    class Growing:
        percent: int = 0


class Syringe(Enum):
    UNKNOWN_CONTENT = auto()
    KNOWN_VACCINE_PROTOTYPE = auto()
