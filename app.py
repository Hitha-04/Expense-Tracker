from flask import Flask
import sqlite3
import os
from config import SECRET_KEY, DATABASE
from routes.auth import auth_bp
from routes.expense import expense_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        with open('database/schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database created successfully!")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)