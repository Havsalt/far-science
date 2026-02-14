from .context import Context


# This is just a type trigger, since `lambda` does not allow assignments
def complete_initial_reports_for_ai(ctx: Context) -> None:
    ctx.state.completed_initial_reports_for_ai = True
