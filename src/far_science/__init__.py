import time
from dataclasses import dataclass

from . import (
    hint,
    actions as _,  # NOTE: Needed to load actions
)
from .action_utils import get_available_actions
from .station import SpaceStation, StationName, Compartment, CompartmentName
from .player import Player
from .dialogue import print_message, get_input_segments
from .questing import Quest


@dataclass
class World:
    player: Player
    all_stations: list[SpaceStation]


world = World(
    all_stations=[
        starting_station := SpaceStation(
            StationName.AKVARIS,
            compartments=[
                starting_compartment := Compartment(
                    CompartmentName.SLEEP_POD,
                    Quest(
                        lambda _: True,
                        [
                            ...,
                            f"It's soOoOoO {hint.wet('cold')} *fht* *fht*",
                            ...,
                            "The backup p~wer isn't enough on its own",
                            "to keep the heater working properly.",
                            ...,
                            f"I should find my way to the {hint.info(CompartmentName.NUCLEAR_REACTOR)}.",
                        ],
                        lambda w: w.player.station.state.has_power,
                        [
                            "Somewhat warmer in here",
                            ...,
                            ...,
                            "... for now at least",
                        ],
                    ),
                    Quest(
                        lambda w: w.player.compartment.is_discovered,
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
                        lambda w: w.player.compartment.is_discovered,
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
                        lambda w: w.player.compartment.is_discovered,
                        [
                            "Still working.",
                            "Should k#ep this running at all costs.",
                        ],
                        lambda w: w.player.station.state.has_power,
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
                        lambda w: w.player.compartment.is_discovered,
                        [
                            "Let's just stay away from the equ!pment for now...",
                            ...,
                            ...,
                            hint.weak("please"),
                        ],
                    ),
                    Quest(
                        lambda w: w.player.station.state.asked_ai_for_help,
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
                        lambda w: w.player.compartment.is_discovered,
                        [
                            f"I {hint.weak("don't")} feel alone in here...",
                            ...,
                            ...,
                            f"{hint.weak('Still')} not alone...",
                            ...,
                        ],
                    ),
                    Quest(
                        lambda w: w.player.station.state.has_power,
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
                        lambda w: w.player.station.state.asked_ai_for_help,
                        [
                            "AI: You got work to do,",
                            f"    wh^ch seems to be aproxim#tly {hint.info('5 science')} reports",
                        ],
                        lambda w: w.player.station.state.science >= 5,
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
                    ),
                ),
                Compartment(
                    CompartmentName.CARGO,
                    Quest(
                        lambda w: w.player.compartment.is_discovered,
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
    ),
)


def main():
    start_message = (
        f"You awake on a {hint.wet('cold')} metal floor.",
        f"{hint.wet('Ice')} is still dripping from your shoulders,",
        f"wh£n you look up and read {hint.label('STATION')} {hint.label(world.player.station.name)} on the wall.",
        ...,
        "Fragments of t&e past, along hardcoded formulas, floats through your mind.",
        f"You slo#ly realize you're in spa?e,  {hint.weak('alone')}.",
        ...,
        f"There might be some {hint.clue('€lues')} around the old projects you w€rked on,",
        f"bef*re the {hint.sprout('V€$^S')}... br.. o.........",
        ...,
        ...,
        "  O\n" + "/ | \\\n" + " / \\",
        f"What will {hint.weak('you')} do now?"
        + " " * 20
        + f"(type '{hint.info('help')}' for list of actions)",
    )
    print_message(start_message, step_time=1.5)

    while True:
        print()
        if world.player.compartment.quest_stage < world.player.compartment.quest_count:
            # Start quest
            if (
                not world.player.compartment.current_quest.is_active
                and world.player.compartment.current_quest.can_start(world)
            ):
                world.player.compartment.current_quest.is_active = True
                if world.player.compartment.current_quest.start_message is not None:
                    time.sleep(1)
                    print_message(*world.player.compartment.current_quest.start_message)
                    time.sleep(1)
                continue  # Idk tbh...

            # End quest - May be instantly after starting - An imidiate quest
            if (
                world.player.compartment.current_quest.is_active
                and world.player.compartment.current_quest.is_completed(world)
            ):
                if world.player.compartment.current_quest.end_message is not None:
                    time.sleep(1)
                    print_message(*world.player.compartment.current_quest.end_message)
                    time.sleep(1)
                world.player.compartment.quest_stage += 1
                continue  # May trigger new quest

        # Perform a valid action
        segments = get_input_segments()
        for action in get_available_actions(world):
            if segments == action.trigger:
                action.fn(world)
                break
        else:  # nobreak
            print(hint.error("Invalid action"))
            continue

        # At the end here, count as 1 cycle/move


if __name__ == "__main__":
    main()
