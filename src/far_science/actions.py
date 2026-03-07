from __future__ import annotations

import random

from . import hint, science, bacteria
from .station import CompartmentName
from .dialogue import pause, print_message, TextLine, Message, Reason
from .action_utils import action, always, anywhere, get_available_actions
from .context import Context
from .player import BONKS_UNTIL_HEAD_TRAUMA
from .state import WaterLevel


@action(anywhere, always, "Read the help manual", alias=["help"])
def read_help(_: Context) -> None:
    print_message(
        "The map is divided into compartments in a linear space.",
        f"You may encounter {hint.invalid('walls')},"
        + f" which {hint.bold('will hinder you from moving')} more in that direction.",
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
    for action in get_available_actions(ctx):
        if action.condition_met(ctx):
            print(
                f"{hint.info(action.description)}:\n- {hint.label(' '.join(action.name_segments))}"
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


def bonk_head(ctx: Context) -> Reason:
    ctx.state.times_bonked_head += 1
    if ctx.state.times_bonked_head >= BONKS_UNTIL_HEAD_TRAUMA:
        ctx.state.times_bonked_head = 0
        bonk_reason: list[TextLine] = [
            f"You bonked your head against the {hint.invalid('wall')},",
            hint.weak("once again."),
        ]
        if ctx.state.science > 0:
            ctx.state.science -= 1
            bonk_reason.extend(
                (
                    ...,
                    "You suffered light head trauma.",
                    hint.weak("-1 science"),
                )
            )
        return bonk_reason

    if random.randint(0, 1):
        return f"A {hint.invalid('wall')} in your way. Nowhere to go..."
    elif random.randint(0, 3):
        return f"That {hint.invalid('wall')} makes this a dead end..."
    else:
        return (
            f"Can't go through {hint.invalid('walls')}...",
            hint.weak("... but sometimes I wish it was possible..."),
        )


def hint_look_around() -> Message:
    return [
        hint.info("TIP")
        + ": After moving into an "
        + hint.bold("undiscovered")
        + " compartment,",
        f"     you can look around by typing {hint.info('i')}.",
        f"     This may {hint.bold('unlock new actions')},",
        f"     which can be viewed using {hint.info('wcid')}.",
    ]


@action(
    anywhere,
    lambda ctx: ctx.compartment.next_compartment is not None,
    "Move forward to the next compartment I find",
    alias=["mf"],
    when_unavailable=bonk_head,
)
def move_forward(ctx: Context) -> None:
    assert ctx.compartment.next_compartment is not None
    ctx.player.compartment = ctx.compartment.next_compartment
    if ctx.compartment.is_discovered:
        print_message("You walked into the " + hint.info(ctx.compartment.name))
    elif not ctx.state.helped_discover_after_move:
        ctx.state.helped_discover_after_move = True
        print_message(hint_look_around())


@action(
    anywhere,
    lambda ctx: ctx.compartment.prev_compartment is not None,
    "Move back into the previous compartment",
    alias=["mb"],
    when_unavailable=bonk_head,
)
def move_backward(ctx: Context) -> None:
    assert ctx.compartment.prev_compartment is not None
    ctx.player.compartment = ctx.compartment.prev_compartment
    if ctx.compartment.is_discovered:
        print_message("You walked back into the " + hint.info(ctx.compartment.name))
    elif not ctx.state.helped_discover_after_move:
        ctx.state.helped_discover_after_move = True
        print_message(hint_look_around())


@action(anywhere, always, alias=["cs"])
def check_science(ctx: Context) -> None:
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
    alias=["s"],
    when_unavailable=(
        lambda ctx: str(ctx.compartment.name)
        + f" is {hint.invalid('no proper place')} to sleep."
    ),
)
def sleep(ctx: Context) -> None:
    ctx.player.action_points = ctx.player.max_action_points
    if ctx.state.water_level.has_active_sprinkling:
        ctx.state.water_level = ctx.state.water_level.next_stage
    if ctx.player.bacteria_stage is bacteria.Stage.Dormant:
        print_message(
            "Quite a comfy cryo-bed.",
            "Feeling rested :)",
        )
    else:
        ctx.player.bacteria_stage.percent += bacteria.GROW_RATE
        if ctx.player.bacteria_stage.percent < 15:
            print_message(
                "Quite a comfy cryo-bed.",
                "Feeling rested :|",
            )
        elif ctx.player.bacteria_stage.percent < 30:
            print_message(
                "Ready for a new day, but somewhat tired",
                ...,
                "... and very thirsty",
            )
        elif ctx.player.bacteria_stage.percent < 40:
            print_message(
                "Woke up,",
                f"and found a new {hint.bacteria('thorn')} sticking out of my hand!",
            )
        elif ctx.player.bacteria_stage.percent < 60:
            print_message(
                "Woke up,",
                f"and found new {hint.bacteria('leafy scales')} covering my legs!",
            )
        elif ctx.player.bacteria_stage.percent < 75:
            print_message(
                "...",
                ...,
                "uaaAAA!!",
                "It hurts in my chest!",
                ...,
                f"I'm turning {hint.bacteria('green')}...",
            )
        elif ctx.player.bacteria_stage.percent < 90:
            print_message(
                "I can't stand this pain anymore!",
                "Waking up was a mistake...",
            )
        elif ctx.player.bacteria_stage.percent >= 100:
            print_message(
                hint.weak("You wake up."),
                ...,
                f"You stay calm and {hint.bacteria('rooted')}.",
                ...,
                ...,
                "At this point...",
                "... would it be wrong to say you're not yourself anymore?",
                ...,
                "Feels like eternity goes by",
                "- and it does...",
                ...,
                "... but you are neither sad, nor happy",
                "because plants have better things to do, than to worry.",
                ...,
                hint.death(
                    f"You found peace in being a plant onboard {hint.label(ctx.station.name)}"
                ),
            )
            exit()
        else:
            print_message(
                "All I can think about",
                ...,
                "... is ending this suffering",
            )


def refuse_science(ctx: Context) -> Reason:
    if ctx.compartment.name is not CompartmentName.SCIENCE_LAB:
        return [
            ctx.compartment.name.article
            + f" is no {hint.invalid('proper place')} for SCIENCE!"
        ]
    if ctx.player.action_points <= 0:
        return [
            f"I'm too {hint.invalid('tired')} for science,"
            + f" and could use some {hint.info('sleep')}",
        ]


@action(
    CompartmentName.SCIENCE_LAB,
    lambda ctx: ctx.player.action_points > 0,
    "Do what I can best, SCIENCE!",
    alias=["ds"],
    when_unavailable=refuse_science,
)
def do_science(ctx: Context) -> None:
    ctx.player.action_points -= 1
    print_message(f"{hint.weak('-1 action point, +1 science')}")
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
    ctx.player.bacteria_stage = bacteria.Stage.Growing(percent=0)


@action(CompartmentName.NUCLEAR_REACTOR, always, "Cause critical reactor overload")
def blow_up(_: Context) -> None:
    print_message(
        "You think you might have seen the inside of a star...",
        ...,
        "Nope.",
        "You just experinced the inside of a uranium core...",
        ...,
        hint.death("Scattered across the universe"),
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
    CompartmentName.AI_GUIDANCE_CENTER,
    lambda ctx: ctx.state.completed_initial_reports_for_ai
    and not ctx.state.learned_about_vaccine_prototype,
    "Read a note laying on one of the panels",
    alias=["read", "note"],
    when_unavailable=lambda ctx: f"There are no notes around in the {ctx.compartment.name}",
)
def read_note_about_vaccine_prototype(ctx: Context) -> None:
    assert ctx.state.syringe is not bacteria.Syringe.KNOWN_VACCINE_PROTOTYPE, (
        "Cannot know about the vaccine until this one-shot action is triggered"
    )
    ctx.state.learned_about_vaccine_prototype = True
    print_message(
        hint.label("== LOG NOTE :: Day 731 =="),
        ...,
        ...,
        "I know what the rules say about this side project of mine,",
        "but it will be in the best interest for the whole crew.",
        ...,
        hint.bacteria("%-{==)---"),
        ...,
        f"Not that I have anything against {hint.clue('her')}",
        f"... but {hint.weak('she')} was the one that gave the order",
        f"- and that's why {hint.weak('she')} should have been more prepared,"
        "for the unkown we are about to discover...",
        ...,
        step_delta=1.5,
    )
    pause(2)
    print_message(
        hint.label("= ABOUT THE VACCINE ="),
        ...,
        f"Since this is a prototype, it is less likely to {hint.weak('cure')}",
        "the bacteria.",
        f"If no {hint.info('hostile bacteria is found, it will attack cardiac systems')}.",
        f"Poor {hint.bold('rat #42')} experienced {hint.info('abnormal increase in heart rythm')}.",
        "In addition, the "
        + hint.info("blood veins coagulated to the point of rupture")
        + ".",
        f"This resulted in the little thing {hint.info('bleeding out')}.",
        ...,
        hint.weak("That was a squeak I won't forget anytime soon..."),
        ...,
        "- S".rjust(60),
        ...,
        step_delta=2,
    )
    pause(4)
    print_message(hint.label("YOU LEARNED ABOUT THE VACCINE PROTOTYPE"))

    if ctx.state.syringe is None:
        pause(2)
        print_message(
            f"One of the {hint.bold('vaccine prototypes')}"
            + f" might still be {hint.info('around somewhere')}...",
        )
    elif ctx.state.syringe is bacteria.Syringe.UNKNOWN_CONTENT:
        pause(2)
        ctx.state.syringe = bacteria.Syringe.KNOWN_VACCINE_PROTOTYPE
        print_message(
            "So that's what's inside of this...",
            ...,
            hint.weak("Might save my life one day"),
        )


@action(
    CompartmentName.MEDICAL_BAY,
    lambda ctx: ctx.compartment.is_discovered
    and not ctx.state.took_syringe
    and ctx.state.syringe is None
    and not ctx.state.learned_about_vaccine_prototype,  # Unknown
    "Pick up a syringe, with unknown content",
    alias=["pick", "up", "syringe"],
)
def pick_up_unknown_syringe(ctx: Context) -> None:
    ctx.state.took_syringe = True
    ctx.state.syringe = bacteria.Syringe.UNKNOWN_CONTENT
    print_message(
        hint.weak("There is a syringe of unknown content on one of the desks."),
        hint.weak("You take it, and look at it."),
        ...,
        "This might be useful,",
        ...,
        hint.weak("but it might kill me under the wrong conditions..."),
        ...,
        hint.bold("- Maybe I can find out more a about it?"),
    )


@action(
    CompartmentName.MEDICAL_BAY,
    lambda ctx: ctx.compartment.is_discovered
    and ctx.state.syringe is None
    and ctx.state.learned_about_vaccine_prototype,  # Known
    "Pick up the vaccine prototype",
    alias=["pick", "up", "vaccine"],
)
def pick_up_known_vaccine(ctx: Context) -> None:
    ctx.state.syringe = bacteria.Syringe.KNOWN_VACCINE_PROTOTYPE
    print_message(
        "The prototype!!",
        "Just lying here on the desk.",
        ...,
        "I'll take that, thank you.",
        ...,
    )


@action(
    anywhere,
    lambda ctx: ctx.state.syringe is bacteria.Syringe.UNKNOWN_CONTENT,
    "Inject syringe",
    alias=["inject", "syringe"],
)
def inject_unknown_syringe(ctx: Context) -> None:
    print_message(
        "Time to find out what this does...",
        ...,
        hint.weak("Injecting syringe"),
        ...,
    )
    if ctx.player.bacteria_stage is bacteria.Stage.Dormant:
        print_message(
            "The world starts to spin.",
            "You look down on your hands, and see your blood begin to bubble.",
            ...,
            "Perhaps there was some crucial condition it required?",
            "... but that doesn't matter anymore...",
            "because you lie on the floor,",
            hint.death("dead") + " - somewhat like a black hole.",
        )
        exit()
    else:
        ctx.player.bacteria_stage.percent = max(
            0,
            ctx.player.bacteria_stage.percent - bacteria.SYRINGE_EFFECT,
        )
        print_message(
            "I feel the blood rushing, like never before!",
            "Feels great.",
        )
    ctx.state.syringe = None  # Remove syringe


@action(
    anywhere,
    lambda ctx: ctx.state.syringe is bacteria.Syringe.KNOWN_VACCINE_PROTOTYPE,
    "Inject vaccine",
)
def inject_vaccine(ctx: Context) -> None:
    if ctx.player.bacteria_stage is bacteria.Stage.Dormant:
        print_message(
            "You either hoped to see your crew again,",
            "or perhaps this was just a moment of stupidity?",
            ...,
            hint.weak("Injecting syringe"),
            ...,
            f"Because there was {hint.info('no')} {hint.bacteria('bacteria')} {hint.info('to fight')},",
            "the contents caused increased heart rhythm,",
            "in conjunction with heavy coagulations.",
            ...,
            "This resulted in, as told, the blood vessels bursting.",
            "You now find yourself bleeding,",
            "without enough oxygen for the brain to function.",
            ...,
            f"You became a {hint.death('dead')} body, drifting through space,"
            "possibly a metaphor to the stars surfing the void",
            "of which is the universe...",
        )
        exit()
    else:
        ctx.player.bacteria_stage.percent = max(
            0,
            ctx.player.bacteria_stage.percent - bacteria.SYRINGE_EFFECT,
        )
        print_message(
            f"This should give me some more time to stop the {hint.bacteria('bacteria')}",
            ...,
            hint.weak("Injecting syringe"),
            hint.weak(f"-{bacteria.SYRINGE_EFFECT}% bacteria"),
        )
    ctx.state.syringe = None  # Remove syringe


@action(
    CompartmentName.CARGO_HOLD,
    lambda ctx: ctx.compartment.is_discovered and not ctx.state.inspected_cargo_soil,
)
def inspect_the_soil(ctx: Context) -> None:
    ctx.state.inspected_cargo_soil = True
    ctx.state.science += 1
    print_message(
        "Looks like the soil is quite fertile,",
        f"possibly of the best quality {hint.weak('ever')} made by man...",
        ...,
        hint.label("YOU LEARNED ABOUT FERTILE SOIL"),
        hint.weak("+1 science"),
    )


def refuse_fetching_soil(ctx: Context) -> Reason:
    if not ctx.state.inspected_cargo_soil:
        return [
            f"I know {hint.invalid('nothing about soil')}.",
            "Why even care about something as basic as old soil?",
        ]
    if ctx.player.action_points <= 0:
        return f"Too {hint.invalid('tired')} for fetching soil."


@action(
    CompartmentName.CARGO_HOLD,
    lambda ctx: ctx.compartment.is_discovered
    and ctx.player.action_points > 0
    and ctx.state.inspected_cargo_soil
    and not ctx.state.fetched_soil,
    "Take some soil, and stuff it in your pockets",
    when_unavailable=refuse_fetching_soil,
)
def take_some_soil(ctx: Context) -> None:
    ctx.state.fetched_soil = True
    ctx.player.action_points -= 1
    print_message(hint.weak("-1 action point"))
    print_message(
        "You take some soil in your pockets,",
        "and walk away with a smile",
        ...,
        "- and dirty clothes",
    )


@action(  # Can be checked multiple times
    CompartmentName.HYDROPONICS_DOME,
    lambda ctx: ctx.compartment.is_discovered,
    "Check the local control panel for status",
    alias=["lcp"],
)
def check_dome_control_panel(ctx: Context) -> None:
    water_hint = hint.ok if ctx.state.water_level.is_good else hint.bad
    power_info = "Power supply: " + (
        hint.ok("online") if ctx.state.has_power else hint.bad("offline")
    )
    water_info = "Water levels: " + water_hint(ctx.state.water_level.pretty_name)
    dirt_info = "Soil quality: " + (
        hint.ok("good") if ctx.state.soil_quality_is_good else hint.bad("bad")
    )
    plant_info = "Plant health: " + (
        hint.ok("growing") if ctx.state.planted_seeds else hint.bad("missing")
    )
    print_message(
        hint.label(f"== STATUS OF {ctx.compartment.name} =="),
        ...,
        power_info,
        water_info,
        dirt_info,
        plant_info,
        step_delta=0.3,
    )
    if (
        not ctx.state.checked_hydroponics_status
    ):  # Oneshot - To trigger "fetch soil" quest
        ctx.state.checked_hydroponics_status = True
        assert not ctx.state.soil_quality_is_good, (
            f"The soil quality cannot be improved before initial {ctx.compartment.name} panel check"
        )
        if ctx.state.inspected_cargo_soil:
            print_message(
                f"I can go back to the {CompartmentName.CARGO_HOLD},"
                "to get some of that high quality soil.",
            )


def refuse_sprinkling(ctx: Context) -> Reason:
    if ctx.state.water_level.has_active_sprinkling:
        return "The sprinklers are" + hint.invalid("already active") + "."
    if not ctx.state.has_power:
        return (
            hint.info("Power")
            + " is "
            + hint.invalid("required")
            + "for the sprinkler to start."
        )


@action(
    CompartmentName.HYDROPONICS_DOME,
    lambda ctx: ctx.compartment.is_discovered
    and ctx.state.has_power
    and not ctx.state.water_level.has_active_sprinkling,
    "Turn on the sprinkling system, to bring these poor plants some water",
    alias=["turn", "on", "sprinkler"],
    when_unavailable=refuse_sprinkling,
)
def turn_on_sprinkling_system(ctx: Context) -> None:
    ctx.state.water_level = WaterLevel.MOISTURE
    print_message(
        hint.weak(
            f"You hear the sound of {hint.wet('water sprinkled')} through the air."
        ),
        ...,
        f"This should help improve the watering {hint.info('over time')}.",
    )


@action(
    CompartmentName.HYDROPONICS_DOME,
    lambda ctx: ctx.state.has_seeds and not ctx.state.planted_seeds,
    f"Plant seeds, in your newly fixed {CompartmentName.HYDROPONICS_DOME}",
    alias=["plant", "seed"],
)
def plant_seeds(ctx: Context) -> None:
    ctx.state.planted_seeds = True
    print_message(
        hint.weak("You planted some seeds."),
        "The new plants should thrive under these top notch conditons.",
    )
