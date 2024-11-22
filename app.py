import os
from flask import Flask, session, redirect, url_for
from model import db  # Import db from model.py to initialize the database
from controller.admin import admin_bp
from controller.customer import customer_bp
from controller.professional import professional_bp
from config import Config
import sqlite3
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with app
db.init_app(app)

# Register Blueprints for different user roles
app.register_blueprint(admin_bp)
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(professional_bp)

@app.route('/')
def home():
    return redirect(url_for('admin.login'))  # Redirect to admin login by default

def database_has_tables(db_path):
    """Check if the database file exists and contains tables."""
    if os.path.exists(db_path):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        connection.close()
        return len(tables) > 0  # Return True if tables exist
    return False

if __name__ == '__main__':
    db_path = os.path.join(app.instance_path, 'database.db')
    os.makedirs(app.instance_path, exist_ok=True)  # Ensure instance folder exists

    if not os.path.exists(db_path) :
        with app.app_context():
            db.create_all()  # Create tables if the database file doesn't exist or is empty
            print("Database initialized with required tables.")
    else:
        print("Database already exists and contains tables. Skipping initialization.")

    app.run(debug=True)