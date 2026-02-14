from .context import Context


# These functions are just a function that mutates the context,
# since `lambda` does not allow assignments


def complete_initial_reports_for_ai(ctx: Context) -> None:
    ctx.state.completed_initial_reports_for_ai = True
