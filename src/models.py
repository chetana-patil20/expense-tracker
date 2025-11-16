from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

DATE_FORMAT = "%Y-%m-%d"

def parse_date(s: str) -> datetime:
    return datetime.strptime(s, DATE_FORMAT)

@dataclass
class Expense:
    id: int
    date: str       # "YYYY-MM-DD"
    amount: float
    category: str
    note: Optional[str] = ""
    kind: str = "expense"   # "expense" or "income"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        # ensure types
        return cls(
            id=int(d["id"]),
            date=str(d["date"]),
            amount=float(d["amount"]),
            category=str(d["category"]),
            note=str(d.get("note", "")),
            kind=str(d.get("kind", "expense"))
        )
