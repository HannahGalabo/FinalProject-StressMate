from dataclasses import dataclass
from datetime import datetime

@dataclass
class StressTier:
    code: str
    status: str
    insight: str
    task: str
    color_hex: str

@dataclass
class StressRecord:
    id: int | None
    user_id: int
    timestamp: str
    level_code: str
    task: str
    note: str

    @classmethod
    def create_new(cls, user_id: int, level_code: str, task: str, note: str):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        clean_note = note.strip() if note.strip() else "No note provided"
        return cls(None, user_id, now_str, level_code, task, clean_note)