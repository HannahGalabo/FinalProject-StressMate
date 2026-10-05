from dataclasses import dataclass

@dataclass
class User:
    id: int | None
    email: str
    password: str