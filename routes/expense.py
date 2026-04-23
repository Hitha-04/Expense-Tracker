from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from models.expense import add_expense, get_expenses, delete_expense, get_category_totals, get_monthly_totals, get_expense_by_id, update_expense, set_budget, get_budget
from datetime import datetime

expense_bp = Blueprint('expense', __name__)

CATEGORIES = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Health', 'Bills', 'Education', 'Other']

def login_required():
    return 'user_id' not in session

@expense_bp.route('/dashboard')
def dashboard():
    if login_required():
        return redirect('/login')
    user_id       = session['user_id']
    month         = request.args.get('month')
    expenses      = get_expenses(user_id, month)
    total         = sum(e['amount'] for e in expenses)
    current_month = month or datetime.now().strftime('%Y-%m')
    budget        = get_budget(user_id, current_month)
    remaining     = round(budget - total, 2) if budget else None
    percent       = min(int((total / budget) * 100), 100) if budget else 0
    return render_template('dashboard.html',
        expenses=expenses, total=total,
        month=month, categories=CATEGORIES,
        budget=budget, remaining=remaining,
        percent=percent, current_month=current_month)

@expense_bp.route('/add', methods=['GET', 'POST'])
def add():
    if login_required():
        return redirect('/login')
    if request.method == 'POST':
        title    = request.form['title']
        amount   = request.form['amount']
        category = request.form['category']
        date     = request.form['date']
        note     = request.form.get('note', '')
        add_expense(session['user_id'], title, float(amount), category, date, note)
        flash('Expense added successfully!', 'success')
        return redirect('/dashboard')
    return render_template('add_expense.html', categories=CATEGORIES)

@expense_bp.route('/delete/<int:expense_id>')
def delete(expense_id):
    if login_required():
        return redirect('/login')
    delete_expense(expense_id, session['user_id'])
    flash('Expense deleted.', 'success')
    return redirect('/dashboard')

@expense_bp.route('/api/chart-data')
def chart_data():
    if login_required():
        return jsonify({})
    user_id        = session['user_id']
    month          = request.args.get('month')
    cat_totals     = get_category_totals(user_id, month)
    monthly_totals = get_monthly_totals(user_id)
    return jsonify({
        'pie': {
            'labels': [r['category'] for r in cat_totals],
            'values': [r['total'] for r in cat_totals]
        },
        'bar': {
            'labels': [r['month'] for r in monthly_totals],
            'values': [r['total'] for r in monthly_totals]
        }
    })

@expense_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit(expense_id):
    if login_required():
        return redirect('/login')
    expense = get_expense_by_id(expense_id, session['user_id'])
    if not expense:
        flash('Expense not found.', 'danger')
        return redirect('/dashboard')
    if request.method == 'POST':
        title    = request.form['title']
        amount   = request.form['amount']
        category = request.form['category']
        date     = request.form['date']
        note     = request.form.get('note', '')
        update_expense(expense_id, session['user_id'], title, float(amount), category, date, note)
        flash('Expense updated successfully!', 'success')
        return redirect('/dashboard')
    return render_template('edit_expense.html', expense=expense, categories=CATEGORIES)

@expense_bp.route('/profile')
def profile():
    if login_required():
        return redirect('/login')
    user_id      = session['user_id']
    expenses     = get_expenses(user_id)
    total        = sum(e['amount'] for e in expenses)
    count        = len(expenses)
    cat_totals   = get_category_totals(user_id)
    top_category = max(cat_totals, key=lambda x: x['total'])['category'] if cat_totals else 'N/A'
    return render_template('profile.html', total=total, count=count, top_category=top_category)

@expense_bp.route('/set-budget', methods=['POST'])
def save_budget():
    if login_required():
        return redirect('/login')
    month  = request.form['month']
    amount = float(request.form['amount'])
    set_budget(session['user_id'], month, amount)
    flash('Budget set successfully!', 'success')
    return redirect('/dashboard?month=' + month)