from __future__ import annotations

import random
from typing import assert_never

from . import hint, science
from .station import CompartmentName
from .dialogue import print_message
from .action_utils import action, always, anywhere, get_available_actions
from .context import Context
from .player import VirusSeverity


@action(anywhere, always, "Read the help manual", alias=["help"])
def read_help(_: Context) -> None:
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
def what_can_i_do(ctx: Context) -> None:
    for action in get_available_actions(ctx.world):
        if action.condition(ctx):
            print(
                f"{hint.info(action.desc)}:\n- {hint.label(' '.join(action.trigger))}"
            )


@action(anywhere, always, "Check what compartment I'm in", alias=["i"])
def where_am_i(ctx: Context) -> None:
    ctx.compartment.is_discovered = True
    print_message(
        "Looks like I'm in "
        + ctx.compartment.name.article
        + " "
        + hint.info(ctx.compartment.name)
        + "..."
    )


@action(
    anywhere,
    lambda ctx: ctx.compartment.next_compartment is not None,
    "Move forward to the next compartment I find",
    alias=["mf"],
)
def move_forward(ctx: Context) -> None:
    assert ctx.compartment.next_compartment is not None
    ctx.player.compartment = ctx.compartment.next_compartment
    if ctx.compartment.is_discovered:
        print_message("You walked into the " + hint.info(ctx.compartment.name))


@action(
    anywhere,
    lambda ctx: ctx.compartment.prev_compartment is not None,
    "Move back into the previous compartment",
    alias=["mb"],
)
def move_backward(ctx: Context) -> None:
    assert ctx.compartment.prev_compartment is not None
    ctx.player.compartment = ctx.compartment.prev_compartment
    if ctx.compartment.is_discovered:
        print_message("You walked back into the " + hint.info(ctx.compartment.name))


@action(anywhere, always, alias=["cs"])
def check_status(ctx: Context) -> None:
    print_message(
        f"Science onboard station {hint.label(ctx.station.name)}:"
        f" {hint.info(str(ctx.state.science))}"
    )


@action(anywhere, always, alias=["ce"])
def check_energy(ctx: Context) -> None:
    print_message(
        f"You have [{hint.info(str(ctx.player.energy).rjust(2))}] energy points left,",
        "... before you need to sleep.",
    )


@action(
    CompartmentName.SLEEP_POD,
    lambda ctx: ctx.compartment.is_discovered,
    "Get some rest",
)
def sleep(ctx: Context) -> None:
    ctx.player.energy = ctx.player.max_energy
    match ctx.player.virus_stage:
        case VirusSeverity.Dormant():
            print_message(
                "I like the smell of fresh cryo-bed.",
                "Feeling rested :)",
            )
        case VirusSeverity.Growing(percent=percent):
            if percent < 15:
                print_message(
                    "I like the smell of fresh cryo-bed.",
                    "Feeling rested :|",
                )
            elif percent < 30:
                print_message(
                    "Ready for a new day,"
                    "but somewhat tired",
                    ...,
                    "... and very thirsty",
                )
            elif percent < 40:
                print_message(
                    "Woke up,"
                    f"and found a new {hint.sprout("thorn")} sticking out of my hand!",
                )
            elif percent < 75:
                print_message(
                    "...",
                    ...,
                    "uaaAAA!!",
                    "It hurts in my chest!",
                    ...,
                    "I'm turning green..."
                )
            else:
                print_message(
                    "I can't stand this pain anymore!",
                    "Waking up was a mistake..."
                )
        case _:
            assert_never(ctx.player.virus_stage)


@action(
    CompartmentName.SCIENCE_LAB,
    lambda ctx: ctx.player.energy > 0,
    "Do what I can best, SCIENCE!",
    alias=["ds"],
)
def do_science(ctx: Context) -> None:
    ctx.player.energy -= 1
    ctx.state.science += 1
    science_message = random.choice(science.MESSAGES)
    colored_science_message = hint.label(science_message)
    print_message(colored_science_message)


@action(
    CompartmentName.NUCLEAR_REACTOR,
    lambda ctx: not ctx.state.has_power,
    "Turn on the reactor",
)
def turn_on_reactor(ctx: Context) -> None:
    ctx.state.has_power = True
    ctx.player.virus_stage = VirusSeverity.Growing(percent=0)


@action(CompartmentName.NUCLEAR_REACTOR, always, "Cause critical reactor overload")
def blow_up(_: Context) -> None:
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
    lambda ctx: ctx.compartment.is_discovered
    and ctx.state.has_power
    and not ctx.state.asked_ai_for_help,
    "The AI might help me if I ask it",
)
def ask_for_help(ctx: Context) -> None:
    ctx.state.asked_ai_for_help = True
    print_message(
        "*ehm*",
        "Hello there AI...",
        "Could you help me?",
        "Do you know what happened here?",
    )
