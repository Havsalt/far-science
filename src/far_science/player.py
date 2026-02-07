from dataclasses import dataclass, field
from typing import final

from .traits import InsideStation, InsideCompartment


class MetaName(type):
    def __str__(self) -> str:
        return self.__name__


@final
class VirusSeverity:
    type Union = type[Dormant] | Growing

    @final
    class Dormant(metaclass=MetaName):
        pass

    @final
    @dataclass
    class Growing:
        percent: int = 0


@dataclass
class Player(
    InsideStation,
    InsideCompartment,
):
    max_energy: int = 3
    energy: int = field(init=False)
    virus_stage: VirusSeverity.Union = VirusSeverity.Dormant

    def __post_init__(self) -> None:
        self.energy = self.max_energy
