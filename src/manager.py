from typing import List, Dict
from src.models import Expense
from collections import defaultdict
from datetime import datetime

class ExpenseManager:
    def __init__(self, storage):
        """
        storage: object implementing methods: all(), add(expense), get(id), update(expense), delete(id)
        """
        self.storage = storage

    def list_expenses(self) -> List[Expense]:
        return self.storage.all()

    def add_expense(self, date: str, amount: float, category: str, note: str = "", kind: str = "expense") -> Expense:
        exp = Expense(id=0, date=date, amount=amount, category=category, note=note, kind=kind)
        return self.storage.add(exp)

    def get(self, expense_id: int):
        return self.storage.get(expense_id)

    def update(self, expense_id: int, **kwargs) -> bool:
        e = self.get(expense_id)
        if not e:
            return False
        for k, v in kwargs.items():
            if hasattr(e, k):
                setattr(e, k, v)
        return self.storage.update(e)

    def delete(self, expense_id: int) -> bool:
        return self.storage.delete(expense_id)

    def summary_by_category(self) -> Dict[str, float]:
        totals = defaultdict(float)
        for e in self.list_expenses():
            amt = e.amount if e.kind == "expense" else -e.amount
            totals[e.category] += amt
        return dict(totals)

    def monthly_totals(self) -> Dict[str, float]:
        totals = defaultdict(float)
        for e in self.list_expenses():
            month = datetime.strptime(e.date, "%Y-%m-%d").strftime("%Y-%m")
            amt = e.amount if e.kind == "expense" else -e.amount
            totals[month] += amt
        return dict(totals)

