from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

professional_bp = Blueprint('professional', __name__, url_prefix='/professional')

# Professional Signup
@professional_bp.route('/professional_signup', methods=['GET', 'POST'])
def professional_signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        service_name = request.form.get('service_name')
        experience = request.form.get('experience')
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        connection = sqlite3.connect('database.db',check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO professionals (email, password, full_name, service_name, experience, address, pincode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email, password, full_name, service_name, experience, address, pincode))
        connection.commit()
        connection.close()

        session['professional_name'] = full_name
        session['user_role'] = 'professional'
        return redirect(url_for('professional.professional_dashboard'))

    return render_template('professional/professional_signup.html')

# Professional Dashboard
@professional_bp.route('/professional_dashboard')
def professional_dashboard():
    return render_template('professional/professional_dashboard.html', user_role='professional')

# Search and Summary Pages
@professional_bp.route('/professional_search')
def professional_search():
    return render_template('professional/professional_search.html')

@professional_bp.route('/professional_summary')
def professional_summary():
    return render_template('professional/professional_summary.html')
