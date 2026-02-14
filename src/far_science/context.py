from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world_gen import World
    from .player import Player
    from .station import Compartment, SpaceStation, StationState


@dataclass(frozen=True)
class Context:
    """
    `Context` about the whole game world and all its most common entities,
    as a "linear" representation.


    """

    world: World
    """The whole game world"""

    @property
    def compartment(self) -> Compartment:
        """Current compartment the player is inside"""
        return self.world.player.compartment

    @compartment.setter
    def compartment(self, value: Compartment) -> None:
        self.world.player.compartment = value

    @property
    def station(self) -> SpaceStation:
        """Current space station that the player is onboard"""
        return self.world.player.station

    @station.setter
    def station(self, value: SpaceStation) -> None:
        self.world.player.station = value

    @property
    def state(self) -> StationState:
        """State of the current space station, that the player is onboard"""
        return self.world.player.station.state

    @state.setter
    def state(self, value: StationState) -> None:
        self.world.player.station.state = value

    @property
    def player(self) -> Player:
        """The one and only player"""
        return self.world.player

    @player.setter
    def player(self, value: Player) -> None:
        self.world.player = value
