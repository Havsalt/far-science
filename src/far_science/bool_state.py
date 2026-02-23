type AnyBool = bool | Bool


class Bool:
    """`Bool` is a thin wrapper around `bool`.

    It adds the method `set`, which makes it mutable in a type safe way,
    while in a `lambda` context.
    This is needed because `lambda` does not natively support `assignment expressions`.
    """

    def __init__(self, variant: bool, /) -> None:
        self.variant = variant

    def set(self, value: bool, /) -> None:
        self.variant = value

    def __bool__(self) -> bool:
        return self.variant
