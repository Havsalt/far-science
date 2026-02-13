from __future__ import annotations

import random
from typing import TYPE_CHECKING

from . import hint, science
from .station import CompartmentName
from .dialogue import print_message
from .action_utils import action, always, anywhere, all_actions, get_available_actions

if TYPE_CHECKING:
    from . import World


@action(anywhere, always, alias=["help"])
def read_help(_: World) -> None:
    print_message(
        "The map is divided into compartments in a linear space.",
        ...,
        "When you want to know what you can do in the current compartment,",
        f"type {hint.info('wcid')}.",
        ...,
        ...,
        f"You can move to other compartments using {hint.info('mf')} and {hint.info('mb')}.",
        "When you enter a new room for the first time,",
        f"you need to check your surrondings using {hint.info('i')}.",
        step_time=0.1,
    )


@action(anywhere, always, "Think about what I can do", alias=["wcid"])
def what_can_i_do(w: World) -> None:
    c = w.player.compartment
    for action in get_available_actions(w):
        if action.condition(w, c):
            print(f"{action.desc}:\n- {' '.join(action.trigger)}")


@action(anywhere, always, alias=["i"])
def where_am_i(w: World) -> None:
    w.player.compartment.is_discovered = True
    print_message(
        "Looks like I'm in "
        + w.player.compartment.name.article
        + " "
        + hint.info(w.player.compartment.name)
        + "..."
    )


@action(
    anywhere,
    lambda _, c: c.next_compartment is not None,
    "Move forward to the next compartment I find",
    alias=["mf"],
)
def move_forward(w: World) -> None:
    assert w.player.compartment.next_compartment is not None
    w.player.compartment = w.player.compartment.next_compartment
    if w.player.compartment.is_discovered:
        print_message("You walked into the " + hint.info(w.player.compartment.name))


@action(
    anywhere,
    lambda _, c: c.prev_compartment is not None,
    "Move back into the previous compartment",
    alias=["mb"],
)
def move_backward(w: World) -> None:
    assert w.player.compartment.prev_compartment is not None
    w.player.compartment = w.player.compartment.prev_compartment
    if w.player.compartment.is_discovered:
        print_message(
            "You walked back into the " + hint.info(w.player.compartment.name)
        )


@action(anywhere, always, alias=["cs"])
def check_status(w: World) -> None:
    print_message(
        f"Science onboard station {hint.label(w.player.station.name)}:"
        f" {hint.info(str(w.player.station.state.science))}"
    )


@action(anywhere, always, alias=["ce"])
def check_energy(w: World) -> None:
    print_message(
        f"You have [{hint.info(str(w.player.energy).rjust(2))}] energy points left,",
        "... before you are put to sleep",
    )


@action(
    CompartmentName.SLEEP_POD,
    lambda _, c: c.is_discovered,
    "Get some rest",
)
def sleep(w: World) -> None:
    w.player.energy = w.player.max_energy
    print_message(
        "I like the smell of fresh cryo-bed.",
        "Feeling rested :)",
    )


@action(
    CompartmentName.SCIENCE_LAB,
    lambda w, _: w.player.energy > 0,
    "Do what I can best, SCIENCE!",
    alias=["ds"],
)
def do_science(w: World) -> None:
    w.player.energy -= 1
    w.player.station.state.science += 1
    science_message = random.choice(science.MESSAGES)
    colored_science_message = hint.label(science_message)
    print_message(colored_science_message)


@action(
    CompartmentName.NUCLEAR_REACTOR,
    lambda w, _: not w.player.station.state.has_power,
    "Turn on the reactor",
)
def turn_on_reactor(w: World) -> None:
    w.player.station.state.has_power = True


@action(CompartmentName.NUCLEAR_REACTOR, always, "Cause critical reactor overload")
def blow_up(w: World) -> None:
    print_message(
        "You think you might have seen the inside of a star...",
        ...,
        "Nope.",
        "You just experinced the inside of a uranium core...",
        ...,
        ...,
        "Dead.",
        step_time=1,
    )
    exit()


@action(
    CompartmentName.AI_GUIDANCE_CENTER,
    lambda w, c: c.is_discovered
    and w.player.station.state.has_power
    and not w.player.station.state.asked_ai_for_help,
    "The AI might help me if I ask it",
)
def ask_for_help(w: World) -> None:
    w.player.station.state.asked_ai_for_help = True
    print_message(
        "*ehm*",
        "Hello there AI...",
        "Could you help me?",
        "Do you know what happened here?",
    )
