from dataclasses import dataclass as _dataclass
from enum import Enum as _Enum, auto as _auto
from typing import Final as _Final, final as _final

from .sentinel import Sentinel as _Sentinel


type _Percent = int
type _NonNegative = int


_DAYS_UNTIL_DEATH: _Final[_NonNegative] = 9
"""A rough estimate on how long it takes for the bacteria to kill."""

GROW_RATE: _Final[_Percent] = 100 // _DAYS_UNTIL_DEATH
SYRINGE_EFFECT: _Final[_NonNegative] = 21


@_final
class Stage:
    """Tagged union.

    Variants:
        - `type[Dormant]`
        - `Growing`
    """

    @_final
    class Dormant(metaclass=_Sentinel): ...

    @_final
    @_dataclass(kw_only=True)
    class Growing:
        percent: int = 0


class Syringe(_Enum):
    UNKNOWN_CONTENT = _auto()
    KNOWN_VACCINE_PROTOTYPE = _auto()
