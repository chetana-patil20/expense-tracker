import csv
import os
from typing import List, Optional
from src.models import Expense

CSV_FIELDS = ["id", "date", "amount", "category", "note", "kind"]

class StorageCSV:
    def __init__(self, path="data/expenses.csv"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()

    def _read_all(self) -> List[Expense]:
        rows = []
        with open(self.path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(Expense.from_dict(r))
        return rows

    def _write_all(self, expenses: List[Expense]):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for e in expenses:
                writer.writerow(e.to_dict())

    def all(self) -> List[Expense]:
        return self._read_all()

    def add(self, expense: Expense) -> Expense:
        expenses = self._read_all()
        max_id = max((e.id for e in expenses), default=0)
        expense.id = max_id + 1
        expenses.append(expense)
        self._write_all(expenses)
        return expense

    def get(self, expense_id: int) -> Optional[Expense]:
        for e in self._read_all():
            if e.id == expense_id:
                return e
        return None

    def update(self, expense: Expense) -> bool:
        expenses = self._read_all()
        for i, e in enumerate(expenses):
            if e.id == expense.id:
                expenses[i] = expense
                self._write_all(expenses)
                return True
        return False

    def delete(self, expense_id: int) -> bool:
        expenses = self._read_all()
        new = [e for e in expenses if e.id != expense_id]
        if len(new) == len(expenses):
            return False
        self._write_all(new)
        return True
