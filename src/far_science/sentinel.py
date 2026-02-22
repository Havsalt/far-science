from typing import final


@final
class Sentinel(type):
    """Type safe `Sentinel`, for declearing sentinel types."""

    __new__: None

    def __repr__(cls) -> str:
        return f"<{__class__.__name__}(<{cls.__name__}>)>"
