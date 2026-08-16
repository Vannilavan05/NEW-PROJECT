import re
import os

app_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports
content = content.replace("from flask_mysqldb import MySQL\n", "")
content = content.replace("import MySQLdb.cursors\n", "import sqlite3\n")

# 2. Initialization
old_init = """# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # XAMPP default is empty
app.config['MYSQL_DB'] = 'sihms_db'

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

mysql = MySQL(app)"""

new_init = """# SQLite Configuration
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
            db.commit()

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
"""
content = content.replace(old_init, new_init)

# 3. Connection and cursor
content = content.replace("cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)", "conn = get_db()\n    cursor = conn.cursor()")
content = content.replace("        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)", "        conn = get_db()\n        cursor = conn.cursor()")
# Since indentation might vary, let's use regex
content = re.sub(r'([ \t]+)cursor = mysql\.connection\.cursor\(MySQLdb\.cursors\.DictCursor\)', r'\1conn = get_db()\n\1cursor = conn.cursor()', content)

# 4. Commit
content = re.sub(r'([ \t]+)mysql\.connection\.commit\(\)', r'\1conn.commit()', content)

# 5. Replace %s with ? for SQL parameters
# To safely replace %s with ?, we only replace inside cursor.execute calls
# Actually, replacing all %s in cursor.execute lines or block is tricky with regex.
# Since it's a small app, replacing '%s' with '?' and "%s" with '?' is probably safe if we assume there are no other uses of %s in SQL strings.
# But what about str % args? It uses %s.
# Let's just replace `%s` with `?` where they are in SQL strings.
content = content.replace('%s', '?')

# Let's see if we have any str formatting `%s` that we broke
# A common issue is `LIKE '%s%%'` -> we might need to fix it if it exists.

# Add init_db call at the bottom
if "if __name__ == '__main__':" in content:
    content = content.replace("if __name__ == '__main__':", "if __name__ == '__main__':\n    init_db()")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
