from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# Customer Signup
@customer_bp.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        address = request.form['address']
        pincode = request.form['pincode']

        connection = sqlite3.connect('database.db', check_same_thread=False)

        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO customers (email, password, full_name, address, pincode)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, password, full_name, address, pincode))
        connection.commit()
        connection.close()

        session['customer_name'] = full_name
        session['user_role'] = 'customer'
        return redirect(url_for('customer.customer_dashboard'))
    
    return render_template('customer/customer_signup.html')

# Customer Dashboard
@customer_bp.route('/customer_dashboard')
def customer_dashboard():
    customer_name = session.get('customer_name', 'Customer')
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    active_services = cursor.fetchall()
    connection.close()

    return render_template('customer/customer_dashboard.html', customer_name=customer_name, active_services=active_services, user_role='customer')

# Subservices and Remarks
@customer_bp.route('/subservices/<main_service>')
def subservices(main_service):
    return render_template('customer/subservices.html', main_service=main_service)

@customer_bp.route('/remarks')
def remarks():
    return render_template('customer/remarks.html')

# Search and Summary Pages
@customer_bp.route('/customer_search')
def customer_search():
    return render_template('customer/customer_search.html')

@customer_bp.route('/customer_summary')
def customer_summary():
    return render_template('customer/customer_summary.html')
