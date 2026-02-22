from dataclasses import dataclass
from typing import Final

from . import quests
from .player import Player
from .station import SpaceStation, StationName, Compartment, CompartmentName


@dataclass
class World:
    player: Player
    all_stations: list[SpaceStation]


# Public export - Mutable and Final
world: Final = World(
    all_stations=[
        starting_station := SpaceStation(
            StationName.AKVARIS,
            compartments=[
                starting_compartment := Compartment(
                    CompartmentName.SLEEP_POD,
                    quests.sleep_pod.turn_on_heater,
                    quests.sleep_pod.inspect_tampering,
                ),
                Compartment(
                    CompartmentName.SCIENCE_LAB,
                    quests.science_lab.discover,
                ),
                Compartment(
                    CompartmentName.NUCLEAR_REACTOR,
                    quests.nuclear_reactor.turn_on_main_power,
                ),
                Compartment(
                    CompartmentName.MEDICAL_BAY,
                    quests.medical_bay.discover,
                    quests.medical_bay.search_for_the_crew,
                ),
                Compartment(
                    CompartmentName.AI_GUIDANCE_CENTER,
                    quests.ai_guidance_center.discover,
                    quests.ai_guidance_center.encounter_ai,
                    quests.ai_guidance_center.complete_initial_reports,
                ),
                Compartment(
                    CompartmentName.CARGO_HOLD,
                    quests.cargo_hold.discover_cargo,
                ),
            ],
        ),
    ],
    player=Player(
        station=starting_station,
        compartment=starting_compartment,
        max_action_points=3,
    ),
)
