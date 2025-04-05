from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserAddSchema:
    user_id: int
    user_group: str | None = None
    user_sections: list | None = None
