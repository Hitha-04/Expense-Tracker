import os

SECRET_KEY = "expense_tracker_secret_123"
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'expenses.db')