from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key for session management

@app.route('/')
def home():
    return redirect(url_for('login'))

# Route for Admin Login page
@app.route('/admin/admin_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Placeholder for verifying admin credentials
        session['user_role'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/admin_login.html')

# Route for Customer Signup page
@app.route('/customer/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        # Get customer details from form
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        address = request.form['address']
        pincode = request.form['pincode']
        
        # Insert new customer into the database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO customers (email, password, full_name, address, pincode)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, password, full_name, address, pincode))
        connection.commit()
        connection.close()
        
        # Save customer name in session and redirect to the dashboard
        session['customer_name'] = full_name
        session['user_role'] = 'customer'
        return redirect(url_for('customer_dashboard'))
    
    return render_template('customer/customer_signup.html')

# Route for Professional Signup page
@app.route('/professional/professional_signup', methods=['GET', 'POST'])
def professional_signup():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        service_name = request.form.get('service_name')
        experience = request.form.get('experience')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        
        # Ensure all fields are filled
        if not all([email, password, fullname, service_name, experience, address, pincode]):
            return "All fields are required.", 400
        
        # Insert data into the database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO professionals (email, password, fullname, service_name, experience, address, pincode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email, password, fullname, service_name, experience, address, pincode))
        connection.commit()
        connection.close()

        # Save session and redirect
        session['professional_name'] = fullname
        session['user_role'] = 'professional'
        return redirect(url_for('professional_dashboard'))

    return render_template('professional/professional_signup.html')

# Route for Customer Dashboard page
@app.route('/customer/customer_dashboard')
def customer_dashboard():
    customer_name = session.get('customer_name', 'Customer')
    active_services = []
    
    # Fetch available services
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT service_name FROM services")
    active_services = cursor.fetchall()
    connection.close()
    
    return render_template(
        'customer/customer_dashboard.html', 
        customer_name=customer_name, 
        active_services=active_services,
        user_role='customer'  # Hardcoded user role
    )

# Route for Professional Dashboard page
@app.route('/professional/professional_dashboard')
def professional_dashboard():
    return render_template('professional/professional_dashboard.html', user_role='professional')  # Hardcoded user role

# Route for Admin Dashboard page
@app.route('/admin/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    # Fetch services to display on the dashboard
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    connection.close()
    
    return render_template(
        'admin/admin_dashboard.html', 
        services=services,
        user_role='admin'  # Hardcoded user role
    )

# Route for New Service page
@app.route('/admin/new_service', methods=['GET', 'POST'])
def new_service():
    if request.method == 'POST':
        # Get new service details from form
        service_name = request.form.get('service_name')
        description = request.form.get('description')
        base_price = request.form.get('base_price')
        
        # Insert new service into the database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO services (service_name, description, base_price)
            VALUES (?, ?, ?)
        ''', (service_name, description, base_price))
        connection.commit()
        connection.close()
        
        # Redirect to Admin Dashboard after adding new service
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/new_service.html')

# Route for Customer Subservices page
@app.route('/customer/subservices/<main_service>')
def subservices(main_service):
    return render_template('customer/subservices.html', main_service=main_service)

# Route for Customer Remarks page
@app.route('/customer/remarks')
def remarks():
    return render_template('customer/remarks.html')

# Route for Search page (Admin)
@app.route('/admin/admin_search')
def admin_search():
    return render_template('admin/admin_search.html')

# Route for Summary page (Admin)
@app.route('/admin/admin_summary')
def admin_summary():
    return render_template('admin/admin_summary.html', user_role='admin')  # Hardcoded user role

# Route for Customer Search page
@app.route('/customer/customer_search')
def customer_search():
    return render_template('customer/customer_search.html')

# Route for Customer Summary page
@app.route('/customer/customer_summary')
def customer_summary():
    return render_template('customer/customer_summary.html')

# Route for Professional Search page
@app.route('/professional/professional_search')
def professional_search():
    return render_template('professional/professional_search.html')

# Route for Professional Summary page
@app.route('/professional/professional_summary')
def professional_summary():
    return render_template('professional/professional_summary.html')

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('customer_name', None)
    session.pop('user_role', None)
    return redirect(url_for('login'))

# Route for Dashboard redirection based on user role
@app.route('/dashboard')
def dashboard():
    user_role = session.get('user_role')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif user_role == 'customer':
        return redirect(url_for('customer_dashboard'))
    elif user_role == 'professional':
        return redirect(url_for('professional_dashboard'))
    else:
        return redirect(url_for('home'))  # Redirect to home if no valid user role in session

if __name__ == '__main__':
    app.run(debug=True)
