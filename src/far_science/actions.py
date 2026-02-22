from __future__ import annotations

import random
from typing import assert_never

from . import hint, science
from .station import CompartmentName, Syringe
from .dialogue import print_message
from .action_utils import action, always, anywhere, get_available_actions
from .context import Context
from .player import VirusStage, VIRUS_GROWING_RATE, SYRINGE_EFFECT


@action(anywhere, always, "Read the help manual", alias=["help"])
def read_help(_: Context) -> None:
    print_message(
        "The map is divided into compartments in a linear space.",
        f"You may encounter {hint.weak('walls')},"
        + " which {hint.weak('will hinder you from moving')} more in that direction.",
        ...,
        "When you want to know what you can do in the current compartment,",
        f"type {hint.info('wcid')}.",
        ...,
        ...,
        f"You can move to other compartments using {hint.info('mf')} and {hint.info('mb')}.",
        "When you enter a new room for the first time,",
        f"you need to check your surrondings using {hint.info('i')}.",
        ...,
        f"Some actions require {hint.info('action points')} ({hint.info('AP')}) to perform.",
        f"You can check how many action points you have by typing {hint.info('ap')}.",
        step_delta=0.1,
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


@action(anywhere, always, alias=["ap"])
def check_action_points(ctx: Context) -> None:
    print_message(
        f"You have {hint.info(f'{ctx.player.action_points} action points')} left,",
        "... before you need to sleep.",
    )


@action(
    CompartmentName.SLEEP_POD,
    lambda ctx: ctx.compartment.is_discovered,
    "Get some rest",
)
def sleep(ctx: Context) -> None:
    ctx.player.action_points = ctx.player.max_action_points
    if ctx.player.virus_stage is VirusStage.Dormant:
        print_message(
            "Quite a comfy cryo-bed.",
            "Feeling rested :)",
        )
    else:
        ctx.player.virus_stage.percent += VIRUS_GROWING_RATE
        if ctx.player.virus_stage.percent < 15:
            print_message(
                "Quite a comfy cryo-bed.",
                "Feeling rested :|",
            )
        elif ctx.player.virus_stage.percent < 30:
            print_message(
                "Ready for a new day, but somewhat tired",
                ...,
                "... and very thirsty",
            )
        elif ctx.player.virus_stage.percent < 40:
            print_message(
                "Woke up,"
                f"and found a new {hint.sprout('thorn')} sticking out of my hand!",
            )
        elif ctx.player.virus_stage.percent < 60:
            print_message(
                "Woke up,"
                f"and found a new {hint.sprout('leafy scales')} covering my legs!",
            )
        elif ctx.player.virus_stage.percent < 75:
            print_message(
                "...",
                ...,
                "uaaAAA!!",
                "It hurts in my chest!",
                ...,
                "I'm turning green...",
            )
        elif ctx.player.virus_stage.percent < 90:
            print_message(
                "I can't stand this pain anymore!",
                "Waking up was a mistake...",
            )
        elif ctx.player.virus_stage.percent >= 100:
            print_message(
                hint.weak("You wake up."),
                ...,
                f"You stay calm and {hint.sprout('rooted')}.",
                ...,
                ...,
                "At this point...",
                "... would it be wrong to say you're not yourself anymore?",
                ...,
                "Feels like eternity goes by",
                "- and it does...",
                ...,
                "... but you are neither sad, nor happy",
                f"because plants have better things to do, than to worry.",
                ...,
                hint.error(
                    f"You found peace in being a plant onboard {hint.label(ctx.station.name)}."
                ),
            )
            exit()
        else:
            print_message(
                "All I can think about",
                ...,
                "... is ending this suffering",
            )


@action(
    CompartmentName.SCIENCE_LAB,
    lambda ctx: ctx.player.action_points > 0,
    "Do what I can best, SCIENCE!",
    alias=["ds"],
)
def do_science(ctx: Context) -> None:
    ctx.player.action_points -= 1
    print_message(f"{hint.weak('-1 action point')}")
    ctx.state.science += 1
    science_message = random.choice(science.MESSAGES)
    colored_science_message = hint.label(science_message)
    print_message(colored_science_message)


@action(
    CompartmentName.NUCLEAR_REACTOR,
    lambda ctx: not ctx.state.has_power,
    "Turn on the reactor",
)  # NOTE: This action *does not* require AP, but will consume 1 if available
def turn_on_reactor(ctx: Context) -> None:
    ctx.state.has_power = True
    if ctx.player.action_points > 0:
        ctx.player.action_points -= 1
        print_message(hint.weak("-1 action point"))
    else:
        print_message(hint.weak("You barley had enough strength to push the button"))
    ctx.player.virus_stage = VirusStage.Growing(percent=0)


@action(CompartmentName.NUCLEAR_REACTOR, always, "Cause critical reactor overload")
def blow_up(_: Context) -> None:
    print_message(
        "You think you might have seen the inside of a star...",
        ...,
        "Nope.",
        "You just experinced the inside of a uranium core...",
        ...,
        ...,
        hint.error("Dead."),
        step_delta=1,
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


@action(
    CompartmentName.MEDICAL_BAY,
    lambda ctx: ctx.compartment.is_discovered,
    "Pick up a syringe, with unknown content",
    alias=["pick", "up", "syringe"],
)
def pick_up_unknown_syringe(ctx: Context) -> None:
    ctx.state.syringe = Syringe.UNKNOWN_CONTENT
    print_message(
        hint.weak("There is a syringe of unknown content on one of the desks."),
        hint.weak("You take it, and look at it."),
        ...,
        "This might be useful,",
        ...,
        hint.weak("but it might kill me under the wrong conditions..."),
        ...,
        hint.weak("Maybe I can find out more a about it?"),
    )


@action(
    anywhere,
    lambda ctx: ctx.state.syringe is not None,
    "Inject syringe",
)
def inject_syringe(ctx: Context) -> None:
    assert ctx.state.syringe is not None, (
        "Mismatch with trigger condition and execution"
    )
    match ctx.state.syringe:
        case Syringe.UNKNOWN_CONTENT:
            print_message(
                "Time to find out what this does...",
                ...,
                hint.weak("Injecting syringe"),
            )
            if ctx.player.virus_stage is VirusStage.Dormant:
                print_message(
                    "The world starts to spin.",
                    "You look down on your hands,and see your skin wither apart.",
                    ...,
                    "Perhaps there was some crucial condition it required?",
                    "... but that doesn't matter anymore...",
                    "because you lie on the floor,",
                    hint.error("dead") + " - somewhat like a black hole.",
                )
                exit()
            else:
                ctx.player.virus_stage.percent = max(
                    0,
                    ctx.player.virus_stage.percent - SYRINGE_EFFECT,
                )
                print_message(
                    "I feel the blood rushing, like never before!",
                    "Feels great.",
                )
        case Syringe.KNOWN_VACCINE_PROTOTYPE:
            if ctx.player.virus_stage is VirusStage.Dormant:
                print_message(
                    "You either hoped to see your crew again,",
                    "or perhaps this was just a moment of stupidity?",
                    ...,
                    hint.weak("Injecting syringe"),
                    ...,
                    f"Because there was {hint.info('no')} {hint.sprout('bacteria')} {hint.info('to fight')},",
                    "the contents caused increased heart rhythm,",
                    "in conjunction with heavy coagulations.",
                    ...,
                    "This resulted in, as told, the blood vessels bursting.",
                    "You now find yourself bleeding,",
                    "without enough oxygen for the brain to function.",
                    ...,
                    f"You became a {hint.error('dead')} body, drifting through space,"
                    "possibly a metaphor to the stars surfing the void",
                    "of which is the universe...",
                )
                exit()
            else:
                ctx.player.virus_stage.percent = max(
                    0,
                    ctx.player.virus_stage.percent - SYRINGE_EFFECT,
                )
                print_message(
                    f"This should give me some more time to stop the {hint.sprout('bacteria')}",
                    ...,
                    hint.weak("Injecting syringe"),
                    ...,
                    hint.weak(f"-{SYRINGE_EFFECT}% bacteria"),
                )
        case _:
            assert_never(ctx.state.syringe)


@action(
    CompartmentName.CARGO,
    lambda ctx: ctx.compartment.is_discovered and not ctx.state.inspected_soil,
)
def inspect_the_soil(ctx: Context) -> None:
    ctx.state.inspected_soil = True
    ctx.state.science += 1
    print_message(
        "Looks like the soil is quite fertile,",
        f"possibly of the best quality {hint.weak('ever')} made by man...",
        ...,
        hint.label("YOU LEARNED ABOUT FERTILE SOIL"),
        hint.weak("+1 science"),
    )
