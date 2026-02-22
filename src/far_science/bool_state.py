type AnyBool = bool | Bool


class Bool:
    def __init__(self, variant: bool, /) -> None:
        self.variant = variant

    def set(self, value: bool, /) -> None:
        self.variant = value

    def __bool__(self) -> bool:
        return self.variant
