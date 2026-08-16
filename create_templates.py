import os

templates_dir = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\templates'

templates_to_create = [
    'index.html',
    'register.html',
    'hospital/dashboard.html',
    'hospital/request_access.html',
    'hospital/view_patients.html',
    'hospital/patient_records.html',
    'hospital/upload_prescription.html',
    'scan_centre/dashboard.html',
    'scan_centre/upload_report.html',
    'scan_centre/view_reports.html',
    'patient/dashboard.html',
    'patient/create_profile.html',
    'patient/view_records.html',
    'patient/manage_approvals.html',
    'pharmacy/dashboard.html',
    'pharmacy/view_prescriptions.html',
    'errors/404.html',
    'errors/403.html',
    'errors/500.html'
]

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placeholder for {filename}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; padding: 2rem; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #2563eb; }}
        .nav {{ margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #e5e7eb; }}
        .nav a {{ margin-right: 1rem; color: #4b5563; text-decoration: none; }}
        .nav a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/login">Login</a>
        <a href="/register">Register</a>
        <a href="/logout">Logout</a>
    </div>
    <h1>{filename}</h1>
    <p>This is a placeholder template because the original file was missing.</p>
</body>
</html>'''

for tpl in templates_to_create:
    filepath = os.path.join(templates_dir, os.path.normpath(tpl))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template.format(filename=tpl))
        print(f"Created {tpl}")
    else:
        print(f"Skipped {tpl} (already exists)")
