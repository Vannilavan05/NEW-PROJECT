import re

app_path = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "cursor = conn.cursor()":
        # Match previous line indentation
        prev_line = lines[i-1]
        indent = len(prev_line) - len(prev_line.lstrip())
        new_lines.append(" " * indent + "cursor = conn.cursor()\n")
    else:
        new_lines.append(line.replace("NOW()", "CURRENT_TIMESTAMP"))

with open(app_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
