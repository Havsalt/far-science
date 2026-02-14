from dataclasses import dataclass, field
from typing import final

from .traits import InsideStation, InsideCompartment


@final
class VirusSeverity:
    @final
    class Dormant:
        def __str__(self) -> str:
            return f"{__class__.__name__}()"

    @final
    @dataclass(kw_only=True)
    class Growing:
        percent: int = 0


@dataclass
class Player(
    InsideStation,
    InsideCompartment,
):
    max_energy: int = 3
    energy: int = field(init=False)
    virus_stage: VirusSeverity.Dormant | VirusSeverity.Growing = VirusSeverity.Dormant()

    def __post_init__(self) -> None:
        self.energy = self.max_energy
