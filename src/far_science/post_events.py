from .context import Context


# These functions are just for mutating the global context,
# since `lambda` does not allow assignments


def complete_initial_reports_for_ai(ctx: Context) -> None:
    ctx.state.completed_initial_reports_for_ai = True
