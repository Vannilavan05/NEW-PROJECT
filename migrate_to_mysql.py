import re
import os

app_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports
content = content.replace("import sqlite3\n", "import sqlite3\nfrom flask_mysqldb import MySQL\nimport MySQLdb.cursors\n")

# 2. Initialization
old_init = """# SQLite Configuration
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with app.open_resource('database_schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()"""

new_init = """# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # XAMPP default is empty
app.config['MYSQL_DB'] = 'sihms_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def get_db():
    return mysql.connection
"""
content = content.replace(old_init, new_init)

# 3. Cursor creation logic
# Find "conn = get_db()\n    cursor = conn.cursor()"
content = re.sub(r'([ \t]+)conn = get_db\(\)\n\1cursor = conn\.cursor\(\)', r'\1conn = get_db()\n\1cursor = conn.cursor()', content)
# We don't actually need to change cursor = conn.cursor() since mysql.connection.cursor() works the same way if configured correctly.
# The previous replace logic was fine. 

# 4. Replace ? with %s
# Only replace ' ?' or '(?' or '?,' or '?)'
content = content.replace(" ?", " %s").replace("(?", "(%s").replace("?,", "%s,").replace("?)", "%s)")
# Let's just do a global replace for all SQL parameters. The exact strings I wrote earlier were `?`.
content = content.replace("= ?", "= %s")
content = content.replace("LIKE ?", "LIKE %s")
content = content.replace("VALUES (%s, %s, %s)", "VALUES (%s, %s, %s)") # Already fixed by global.
# Just doing a global replace of '?' that are standalone.
import re
content = re.sub(r'\?', '%s', content)

# 5. Remove init_db call
content = content.replace("init_db()\n    ", "")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Update database schema for MySQL
schema_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\database_schema.sql'
with open(schema_path, 'r', encoding='utf-8') as f:
    schema_content = f.read()

schema_content = schema_content.replace('AUTOINCREMENT', 'AUTO_INCREMENT')

with open(schema_path, 'w', encoding='utf-8') as f:
    f.write(schema_content)

print("Migration to MySQL complete.")
