from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Login
@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_role'] = 'admin'
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/admin_login.html')

# Admin Dashboard
@admin_bp.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('user_role') != 'admin':
        return redirect(url_for('admin.login'))

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    
    services = cursor.fetchall()
    connection.close()

    return render_template('admin/admin_dashboard.html', services=services, user_role='admin')

# Add a New Service
@admin_bp.route('/new_service', methods=['GET', 'POST'])
def new_service():
    if session.get('user_role') != 'admin':
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        service_name = request.form.get('service_name')
        description = request.form.get('description')
        base_price = request.form.get('base_price')

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO services(service_name, description, base_price)
            VALUES (?, ?, ?)
        ''', (service_name, description, base_price))
        connection.commit()
        connection.close()

        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/new_service.html')

# Search and Summary Pages
@admin_bp.route('/admin_search')
def admin_search():
    return render_template('admin/admin_search.html')

@admin_bp.route('/admin_summary')
def admin_summary():
    return render_template('admin/admin_summary.html', user_role='admin')
