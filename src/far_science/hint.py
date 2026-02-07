from typing import Final as _Final


type _Color = str
type _ColorCode = int | str
_ANSI_RESET: _Final[_Color] = "\x1b[0m"


class _Hint:
    def __init__(self, color: _ColorCode) -> None:
        self._color: _Color = f"\x1b[{color}m"

    def __call__(self, text: str) -> _Color:
        self._text = str(text)  # Wrap in `str` to fix `StrEnum` with custom `__str__`
        return self._color + self._text + _ANSI_RESET

    def __repr__(self) -> str:
        assert hasattr(self, "_text"), f"Hint({self._color!r}) was never called"
        return super().__repr__()


clue = _Hint(35)  # Lore related
weak = _Hint(3)
label = _Hint(33)
wet = _Hint(34)
sprout = _Hint(32)
info = _Hint(36)
error = _Hint(31)
