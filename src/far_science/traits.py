from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .station import Compartment, SpaceStation


@dataclass
class HasHealth:
    health: int


@dataclass
class HasDamage:
    damage: int


@dataclass
class HasName[T = str]:
    name: T


@dataclass
class InsideCompartment:
    compartment: Compartment


@dataclass
class InsideStation:
    station: SpaceStation
