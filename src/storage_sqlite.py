import sqlite3
import os
from typing import List, Optional
from src.models import Expense

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    note TEXT,
    kind TEXT DEFAULT 'expense'
);
"""

class StorageSQLite:
    def __init__(self, path="data/expenses.db"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        with self.conn:
            self.conn.execute(CREATE_TABLE_SQL)

    def all(self) -> List[Expense]:
        cur = self.conn.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
        rows = cur.fetchall()
        return [Expense.from_dict(dict(r)) for r in rows]

    def add(self, expense: Expense) -> Expense:
        cur = self.conn.execute(
            "INSERT INTO expenses (date, amount, category, note, kind) VALUES (?, ?, ?, ?, ?)",
            (expense.date, expense.amount, expense.category, expense.note, expense.kind)
        )
        expense.id = cur.lastrowid
        self.conn.commit()
        return expense

    def get(self, expense_id: int) -> Optional[Expense]:
        cur = self.conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        return Expense.from_dict(dict(row)) if row else None

    def update(self, expense: Expense) -> bool:
        cur = self.conn.execute(
            "UPDATE expenses SET date=?, amount=?, category=?, note=?, kind=? WHERE id=?",
            (expense.date, expense.amount, expense.category, expense.note, expense.kind, expense.id)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def delete(self, expense_id: int) -> bool:
        cur = self.conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()
        return cur.rowcount > 0
