from . import (
    hint,
    actions as _,  # NOTE: Needed to load actions
)
from .action_utils import get_available_actions, get_action_by_name
from .dialogue import TEXT_LINE_TYPES, print_message, get_input_segments, pause
from .context import Context
from .world_gen import world


# NOTE: Use env flag `FAR_SCIENCE_INSTANT_TEXT` to skip sleep between text lines


def main():
    ctx = Context(world)
    start_message = (
        f"You awake on a {hint.wet('cold')} metal floor.",
        f"{hint.wet('Ice')} is still dripping from your shoulders,",
        f"wh£n you look up and read {hint.label('STATION')} {hint.label(ctx.station.name)} on the wall.",
        ...,
        "Fragments of t&e past, along hardcoded formulas, floats through your mind.",
        f"You slo#ly realize you're in spa?e,  {hint.weak('alone')}.",
        ...,
        f"There might be some {hint.clue('€lues')} around the old projects you w€rked on,",
        f"bef*re the {hint.bacteria('B$€^E...')} br... o....",
        ...,
        ...,
        hint.wet("  O\n" + "/ | \\\n" + " / \\"),
        f"What will {hint.weak('you')} do now?"
        + " " * 20
        + f"(type '{hint.info('help')}' for list of actions)",
    )
    print_message(start_message, step_delta=1.5)

    while True:
        print()
        if world.player.compartment.quest_stage < world.player.compartment.quest_count:
            # Start quest
            if (
                not world.player.compartment.current_quest.is_active
                and world.player.compartment.current_quest.can_start(ctx)
            ):
                world.player.compartment.current_quest.is_active = True
                if world.player.compartment.current_quest.start_message is not None:
                    pause(1)
                    print_message(*world.player.compartment.current_quest.start_message)
                    pause(1)
                continue  # Idk tbh...

            # End quest - May be instantly after started - An imidiate quest
            if (
                world.player.compartment.current_quest.is_active
                and world.player.compartment.current_quest.is_completed(ctx)
            ):
                if world.player.compartment.current_quest.end_message is not None:
                    pause(1)
                    print_message(*world.player.compartment.current_quest.end_message)
                    pause(1)
                if world.player.compartment.current_quest.post_event is not None:
                    world.player.compartment.current_quest.post_event(ctx)
                world.player.compartment.quest_stage += 1
                continue  # May trigger new quest

        # Perform a valid action
        segments = get_input_segments()
        for action in get_available_actions(ctx):
            if segments == action.name_segments:
                action.perform(ctx)
                break
        else:  # nobreak
            if action := get_action_by_name(segments):
                if action.when_unavailable:
                    reason = action.when_unavailable(ctx) or hint.error(
                        "Unavailable action"
                    )
                else:
                    reason = hint.error("Unavailable action")
            else:
                reason = hint.error("Invalid action")
            print_message(reason)
            continue

        # At the end here, count as 1 cycle/move


if __name__ == "__main__":
    main()
