from flask import Blueprint, render_template, request, redirect, url_for, session,flash
import sqlite3
from model import Service,ServiceRequest,Professional, db
from config import SUBSERVICES


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

        connection = sqlite3.connect('instance/database.db', check_same_thread=False)

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

@customer_bp.route('/book_service/<int:service_id>', methods=['POST', 'GET'])
def book_service(service_id):
    customer_id = session.get('customer_id', 1)  # Replace with actual customer authentication
    status = "Requested"

    # Determine the service_name from the SUBSERVICES mapping
    name = None
    for main_service, subservices in SUBSERVICES.items():
        if service_id in subservices:
            name = subservices[service_id]  # Get the subservice name
            break
    
    if not name:
        name = None

    # Create a new ServiceRequest instance
    new_request = ServiceRequest(
        service_id=service_id,
        customer_id=customer_id,
        name=name,
        status=status
    )

    # Add the new request to the session and commit the transaction
    db.session.add(new_request)
    db.session.commit()

    return redirect(url_for('customer.customer_dashboard'))
@customer_bp.route('/customer_dashboard')
def customer_dashboard():
    # Replace `1` with actual logic for authenticated customer_id
    customer_id = session.get('customer_id', 1)  # Hardcoded to 1 for now

    # Query service requests for this customer
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()

    # Pass the service requests directly to the template
    return render_template('customer/customer_dashboard.html', service_requests=service_requests)

@customer_bp.route('/subservices/<main_service>', methods=['GET'])
def subservices(main_service):
    return render_template('customer/subservices.html', subservices=SUBSERVICES, main_service=main_service)


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
