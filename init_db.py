import sqlite3

def initialize_db():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Create professionals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professionals (
                professional_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                fullname TEXT NOT NULL,
                service_name TEXT NOT NULL,
                experience INTEGER NOT NULL,
                address TEXT,
                pincode INTEGER
            )
        ''')
        print("Professionals table created successfully")

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT,
            address TEXT,
            pincode NUM
        )
    ''')
        print("Customers table created successfully")
        
        cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT,
    base_price REAL NOT NULL,
    status TEXT DEFAULT 'Active',
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')
        print("Services table created successfully")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error creating database:", e)



if __name__ == '__main__':
    initialize_db()
    print("Database initialized with required tables.")
