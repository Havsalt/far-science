import time

from . import (
    hint,
    actions as _,  # NOTE: Needed to load actions
)
from .action_utils import get_available_actions
from .dialogue import print_message, get_input_segments
from .context import Context
from .world_gen import world


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
        # Always use new and updated context namespace for each cycle/half-cycle
        ctx = Context(world)
        print()
        if world.player.compartment.quest_stage < world.player.compartment.quest_count:
            # Start quest
            if (
                not world.player.compartment.current_quest.is_active
                and world.player.compartment.current_quest.can_start(ctx)
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
                and world.player.compartment.current_quest.is_completed(ctx)
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
                action.fn(ctx)
                break
        else:  # nobreak
            print(hint.error("Invalid action"))
            continue

        # At the end here, count as 1 cycle/move


if __name__ == "__main__":
    main()
