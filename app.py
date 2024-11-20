from flask import Flask, session, redirect, url_for
from model import db  # Import db from model.py to initialize the database
from controller.admin import admin_bp
from controller.customer import customer_bp
from controller.professional import professional_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key for session management

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

# Initialize the database with app
db.init_app(app)

# Register Blueprints for different user roles
app.register_blueprint(admin_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(professional_bp)

@app.route('/')
def home():
    return redirect(url_for('admin.login'))  # Redirect to admin login by default

# Explicitly creating the database in the main block
with app.app_context():
    db.create_all()  # Create all tables defined in model.py
    print("Database initialized with required tables.")

if __name__ == '__main__':
    app.run(debug=True)
