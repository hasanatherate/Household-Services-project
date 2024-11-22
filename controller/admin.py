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

    # Fetch data from the database
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()
    
    # Fetch services data
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    
    # Fetch professionals data
    cursor.execute("SELECT * FROM professionals")
    professionals = cursor.fetchall()
    
    # Fetch service requests data
    cursor.execute("SELECT * FROM service_requests")
    service_requests = cursor.fetchall()
    
    connection.close()

    return render_template('admin/admin_dashboard.html', 
                           services=services, 
                           professionals=professionals,
                           service_requests=service_requests,
                           user_role='admin')


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

@admin_bp.route('/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('admin.login'))

    # Connect to the database
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()

    # Delete the service by ID
    cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if session.get('user_role') != 'admin':
        return redirect(url_for('admin.login'))
    
    connection = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connection.cursor()

    if request.method == 'POST':
        # Update the service details in the database
        service_name = request.form['service_name']
        description = request.form['description']
        base_price = request.form['base_price']

        cursor.execute('''
            UPDATE services
            SET service_name = ?, description = ?, base_price = ?
            WHERE id = ?
        ''', (service_name, description, base_price, service_id))
        connection.commit()
        connection.close()
        
        return redirect(url_for('admin.admin_dashboard'))
    
    # Fetch the service details for pre-filling the form
    cursor.execute("SELECT service_name, description, base_price FROM services WHERE id = ?", (service_id,))
    service = cursor.fetchone()
    connection.close()

    return render_template('admin/new_service.html', service_id=service_id, service=service)

# Search and Summary Pages
@admin_bp.route('/admin_search')
def admin_search():
    return render_template('admin/admin_search.html')

@admin_bp.route('/admin_summary')
def admin_summary():
    return render_template('admin/admin_summary.html', user_role='admin')
