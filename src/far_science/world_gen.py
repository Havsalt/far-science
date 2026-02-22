from dataclasses import dataclass
from typing import Final

from . import hint
from .player import Player
from .station import SpaceStation, StationName, Compartment, CompartmentName
from .action_utils import always
from .questing import Quest


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
                    Quest(
                        always,
                        [
                            ...,
                            f"It's soOoOoO {hint.wet('cold')} *fht* *fht*",
                            ...,
                            "The backup p~wer isn't enough on its own",
                            "to keep the heater working properly.",
                            ...,
                            f"I should find my way to the {hint.info(CompartmentName.NUCLEAR_REACTOR)}.",
                        ],
                        lambda ctx: ctx.state.has_power,
                        [
                            "Somewhat warmer in here",
                            ...,
                            ...,
                            "... for now at least",
                        ],
                    ),
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            f"There are s?gns of {hint.clue('tampering')} with the {hint.wet('cryo-pod')}.",
                            ...,
                            hint.weak("Who could have done this?"),
                            ...,
                        ],
                    ),
                ),
                Compartment(
                    CompartmentName.SCIENCE_LAB,
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            "Used to be caught up in some report or project.",
                            "It was fun while it last~d...",
                            ...,
                            hint.weak("Really miss doing some")
                            + " "
                            + hint.info("science")
                            + "...",
                            ...,
                        ],
                    ),
                ),
                Compartment(
                    CompartmentName.NUCLEAR_REACTOR,
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            "Still working.",
                            "Should k#ep this running at all costs.",
                        ],
                        lambda ctx: ctx.state.has_power,
                        [
                            "*Pushed power button*",
                            ...,
                            f"{hint.clue('Voice')}: Power, online",
                        ],
                    ),
                ),
                Compartment(
                    CompartmentName.MEDICAL_BAY,
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            "Let's just stay away from the equ!pment for now...",
                            ...,
                            ...,
                            hint.weak("please"),
                        ],
                    ),
                    Quest(
                        lambda ctx: ctx.state.asked_ai_for_help
                        and ctx.state.completed_initial_reports_for_ai,
                        [
                            "Well,",
                            "there are nobody here...",
                            ...,
                            f"... and who even is this {hint.weak('Snidri')}!",
                            ...,
                            ...,
                            f"For all I know, {hint.weak('"the crew"')} might not even be real,",
                            hint.weak("perhaps only imaginative friends?"),
                            ...,
                            "... but people of the imagination does certainly not",
                            f"leave {hint.clue('notes')} like {hint.weak('these')} scattered around.",
                        ],
                    ),
                ),
                Compartment(
                    CompartmentName.AI_GUIDANCE_CENTER,
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            f"I {hint.weak("don't")} feel alone in here...",
                            ...,
                            ...,
                            f"{hint.weak('Still')} not alone...",
                            ...,
                        ],
                    ),
                    Quest(
                        lambda ctx: ctx.state.has_power,
                        [
                            f"{hint.clue('Voice')}: Hello there... *bzZt*",
                            ...,
                            f"You have been gone for {hint.clue('-27429999...')}"
                            + f" {hint.error('ERROR: Malformed number')}",
                            ...,
                            hint.weak("Me: *hmm*"),
                            hint.weak("    A working AI on the station?"),
                            ...,
                        ],
                    ),
                    Quest(
                        lambda ctx: ctx.state.asked_ai_for_help,
                        [
                            "AI: You got work to do,",
                            f"    wh^ch seems to be aproxim#tly {hint.info('5 science')} reports",
                        ],
                        lambda ctx: ctx.state.science >= 5,
                        [
                            "AI: Acceptable work.",
                            ...,
                            f"AI: Unlike the rest of the {hint.clue('crew')}...",
                            f"    They have been l1ttle productive for the last {hint.error('<BAD TIMESPAN>')}",
                            ...,
                            "Me: Crew?",
                            ...,
                            "AI: There is a lot of work to catch up with,",
                            "    since nobody else is as c$pable as you in the lab.",
                            ...,
                            ...,
                            f"AI: Check if {hint.clue('Snidri')} is done with his {hint.sprout('project')}"
                            + f" in the {hint.label(CompartmentName.MEDICAL_BAY)}.",
                            "    He is long over schedule... *bzZt*",
                        ],
                        post_event=lambda ctx: ctx.state.completed_initial_reports_for_ai.set(
                            True
                        ),
                    ),
                ),
                Compartment(
                    CompartmentName.CARGO,
                    Quest(
                        lambda ctx: ctx.compartment.is_discovered,
                        [
                            f"Can't seem to remember why we had so much {hint.clue('soil')} with us.",
                            "Were we gonna terraform Marz or something?",
                        ],
                    ),
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
