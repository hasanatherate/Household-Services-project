import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance/database.db')}"  # Ensures the database is in 'instance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'  # Replace with a secure key

SUBSERVICES = {
    "Cleaning": {
        4: "Home Cleaning",
        5: "Office Cleaning",
        6: "Carpet Cleaning",
    },
    "Electrical": {
        10: "Wiring",
        11: "Lighting Installation",
        12: "Electrical Repair",
    },
    "AC Repair": {
        1: "AC Installation",
        2: "AC Maintenance",
        3: "AC Cleaning",
    },
    "Salon": {
        7: "Haircut",
        8: "Facial",
        9: "Manicure",
    }
}
