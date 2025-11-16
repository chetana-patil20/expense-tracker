import sys
from tabulate import tabulate
from src.storage_csv import StorageCSV
from src.storage_sqlite import StorageSQLite
from src.manager import ExpenseManager
from datetime import datetime

def choose_storage():
    print("Choose storage:")
    print("1) CSV (data/expenses.csv)")
    print("2) SQLite (data/expenses.db)")
    choice = input("Enter 1 or 2 (default 1): ").strip() or "1"
    return StorageCSV() if choice == "1" else StorageSQLite()

def print_expenses(expenses):
    if not expenses:
        print("No records.")
        return
    rows = [[e.id, e.date, e.kind, f"{e.amount:.2f}", e.category, e.note] for e in expenses]
    print(tabulate(rows, headers=["ID","Date","Type","Amount","Category","Note"]))

def main():
    storage = choose_storage()
    mgr = ExpenseManager(storage)

    MENU = """
1) List expenses
2) Add expense/income
3) Update record
4) Delete record
5) Summary by category
6) Monthly totals
0) Exit
"""
    while True:
        print(MENU)
        opt = input("Choose: ").strip()
        if opt == "1":
            print_expenses(mgr.list_expenses())
        elif opt == "2":
            kind = input("Type (expense/income) [expense]: ").strip() or "expense"
            date = input("Date (YYYY-MM-DD) [today]: ").strip() or datetime.today().strftime("%Y-%m-%d")
            amount = float(input("Amount: ").strip())
            cat = input("Category: ").strip()
            note = input("Note: ").strip()
            e = mgr.add_expense(date=date, amount=amount, category=cat, note=note, kind=kind)
            print("Added:", e)
        elif opt == "3":
            eid = int(input("Record ID to update: ").strip())
            e = mgr.get(eid)
            if not e:
                print("Not found.")
                continue
            print("Leave blank to keep current.")
            date = input(f"Date ({e.date}): ").strip() or e.date
            amount_s = input(f"Amount ({e.amount}): ").strip()
            amount = float(amount_s) if amount_s else e.amount
            cat = input(f"Category ({e.category}): ").strip() or e.category
            note = input(f"Note ({e.note}): ").strip() or e.note
            kind = input(f"Type ({e.kind}): ").strip() or e.kind
            ok = mgr.update(eid, date=date, amount=amount, category=cat, note=note, kind=kind)
            print("Updated." if ok else "Failed.")
        elif opt == "4":
            eid = int(input("Record ID to delete: ").strip())
            ok = mgr.delete(eid)
            print("Deleted." if ok else "Not found.")
        elif opt == "5":
            s = mgr.summary_by_category()
            rows = [[k, f"{v:.2f}"] for k,v in s.items()]
            print(tabulate(rows, headers=["Category","Total (negative = income)"]))
        elif opt == "6":
            s = mgr.monthly_totals()
            rows = [[k, f"{v:.2f}"] for k,v in sorted(s.items())]
            print(tabulate(rows, headers=["Month","Total"]))
        elif opt == "0":
            print("Bye.")
            sys.exit(0)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
