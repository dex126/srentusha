from dataclasses import dataclass


@dataclass(slots=True)
class User:
    user_id: int
    user_group: str | None = None
    user_sections: list | None = None
