from flask import Blueprint, render_template, request, redirect, url_for, session,flash
import sqlite3
from model import Service,ServiceRequest, db
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

@customer_bp.route('/book_service/<int:service_id>', methods=['POST', 'GET'])
def book_service(service_id):
    customer_id = 1  # Replace with actual customer ID once authentication is implemented
    status = "Requested"

    # Insert the service request into the database
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()

    query = """
    INSERT INTO service_requests (customer_id, service_id,status)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (customer_id, service_id,status))
    connection.commit()
    connection.close()

    return redirect(url_for('customer.customer_dashboard'))
@customer_bp.route('/customer_dashboard')
def customer_dashboard():
    # Replace `1` with actual logic for authenticated customer_id
    customer_id = session.get('customer_id', 1)  # Hardcoded to 1 for now

    # Query service requests for this customer
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()

    # Map service requests to include service name from the config file
    service_data = []
    for request in service_requests:
        # Get main service and subservices mapping from the config
        main_service = None
        subservices = None
        for service, subs in SUBSERVICES.items():
            if request.service_id in subs:
                main_service = service
                subservices = subs
                break

        service_name = subservices.get(request.service_id, "Unknown") if subservices else "Unknown"

        # Append details to service_data
        service_data.append({
            "service_request_id": request.id,
            "service_name": service_name,
            "status": request.status,
            "date_requested": request.date_requested,
        })

    return render_template('customer/customer_dashboard.html', service_data=service_data)
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
