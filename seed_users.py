import sqlite3
from werkzeug.security import generate_password_hash

db_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

users_to_create = [
    ('hospital1', 'password123', 'hospital', 'City Hospital'),
    ('patient1', 'password123', 'patient', ''),
    ('pharmacy1', 'password123', 'pharmacy', 'Quick Meds'),
    ('scan1', 'password123', 'scan_centre', 'Advanced Scans')
]

for username, password, role, org in users_to_create:
    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute('''
            INSERT INTO users (username, password, role, organization) 
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_pw, role, org))
        print(f"Created user: {username}")
    except sqlite3.IntegrityError:
        print(f"User {username} already exists.")

conn.commit()
conn.close()
