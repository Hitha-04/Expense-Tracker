import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def register_user(username, email, password):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password))
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

def login_user(email, password):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    db.close()
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None