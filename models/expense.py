import sqlite3
from config import DATABASE
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def add_expense(user_id, title, amount, category, date, note):
    db = get_db()
    db.execute(
        "INSERT INTO expenses (user_id, title, amount, category, date, note) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, title, amount, category, date, note)
    )
    db.commit()
    db.close()

def get_expenses(user_id, month=None):
    db = get_db()
    if month:
        expenses = db.execute(
            "SELECT * FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ? ORDER BY date DESC",
            (user_id, month)
        ).fetchall()
    else:
        expenses = db.execute(
            "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        ).fetchall()
    db.close()
    return expenses

def delete_expense(expense_id, user_id):
    db = get_db()
    db.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    )
    db.commit()
    db.close()

def get_category_totals(user_id, month=None):
    db = get_db()
    if month:
        rows = db.execute(
            "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? AND strftime('%Y-%m', date) = ? GROUP BY category",
            (user_id, month)
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category",
            (user_id,)
        ).fetchall()
    db.close()
    return rows

def get_monthly_totals(user_id):
    db = get_db()
    rows = db.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY month ORDER BY month",
        (user_id,)
    ).fetchall()
    db.close()
    return rows

def get_expense_by_id(expense_id, user_id):
    db = get_db()
    expense = db.execute(
        "SELECT * FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    ).fetchone()
    db.close()
    return expense

def update_expense(expense_id, user_id, title, amount, category, date, note):
    db = get_db()
    db.execute(
        "UPDATE expenses SET title=?, amount=?, category=?, date=?, note=? WHERE id=? AND user_id=?",
        (title, amount, category, date, note, expense_id, user_id)
    )
    db.commit()
    db.close()

def set_budget(user_id, month, amount):
    db = get_db()
    db.execute(
        "INSERT INTO budgets (user_id, month, amount) VALUES (?, ?, ?) ON CONFLICT(user_id, month) DO UPDATE SET amount=?",
        (user_id, month, amount, amount)
    )
    db.commit()
    db.close()

def get_budget(user_id, month):
    db = get_db()
    row = db.execute(
        "SELECT amount FROM budgets WHERE user_id = ? AND month = ?",
        (user_id, month)
    ).fetchone()
    db.close()
    return row['amount'] if row else None