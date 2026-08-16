import os

templates_dir = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\templates'
templates = {}

# --- SCAN CENTRE ---
templates['scan_centre/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Scan Centre Dashboard{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-x-ray text-primary me-2"></i> Scan Centre Dashboard</h2>
<div class="row">
    <div class="col-md-6 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-info">{{ stats.total_scans }}</h1>
            <p class="text-muted fw-medium mb-3">Total Scans Uploaded</p>
            <a href="/scan_centre/reports" class="btn btn-outline-info rounded-pill">View All Uploads</a>
        </div>
    </div>
    <div class="col-md-6 mb-4">
        <div class="glass-card p-5 text-center d-flex flex-column align-items-center justify-content-center h-100 border-primary border-2" style="border-style: dashed;">
            <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
            <h4 class="fw-bold">Upload New Report</h4>
            <a href="/scan_centre/upload-report" class="btn btn-primary rounded-pill mt-2 stretched-link px-4">Upload Now</a>
        </div>
    </div>
</div>
{% endblock %}'''

templates['scan_centre/upload_report.html'] = '''{% extends "base.html" %}
{% block title %}Upload Scan Report{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="glass-card p-5">
            <h3 class="fw-bold mb-4 text-center">Upload Scan Report</h3>
            <form method="POST" enctype="multipart/form-data">
                <div class="mb-4">
                    <label class="form-label fw-medium">Patient ID or QR Code String</label>
                    <input type="text" class="form-control" name="patient_id_or_qr" required placeholder="e.g. SIHMS_12_168...">
                </div>
                <div class="mb-4">
                    <label class="form-label fw-medium">Scan Type</label>
                    <select class="form-select form-control" name="scan_type" required>
                        <option value="X-Ray">X-Ray</option>
                        <option value="MRI">MRI</option>
                        <option value="CT Scan">CT Scan</option>
                        <option value="Ultrasound">Ultrasound</option>
                        <option value="Blood Test">Blood Test Report</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-medium">Diagnosis / Summary</label>
                    <textarea class="form-control" name="diagnosis" rows="3" placeholder="Brief summary of findings..."></textarea>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-medium">Report File (PDF/Image)</label>
                    <input type="file" class="form-control" name="report_file" required>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill"><i class="fas fa-upload me-2"></i> Upload Report to Patient Profile</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}'''

templates['scan_centre/view_reports.html'] = '''{% extends "base.html" %}
{% block title %}Uploaded Reports{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4">Uploaded Reports</h2>
<div class="glass-card p-4">
    <div class="table-responsive">
        <table class="table align-middle">
            <thead class="table-light">
                <tr>
                    <th>Date</th>
                    <th>Patient ID</th>
                    <th>Scan Type</th>
                    <th>Diagnosis</th>
                    <th>File</th>
                </tr>
            </thead>
            <tbody>
                {% for scan in scans %}
                <tr>
                    <td>{{ scan.created_at }}</td>
                    <td class="fw-bold text-primary">#{{ scan.patient_id }}</td>
                    <td><span class="badge bg-info text-dark rounded-pill">{{ scan.scan_type }}</span></td>
                    <td>{{ scan.diagnosis }}</td>
                    <td>
                        <a href="/uploads/{{ scan.report_path }}" target="_blank" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                            <i class="fas fa-external-link-alt me-1"></i> View
                        </a>
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="5" class="text-center py-4 text-muted">No scan reports uploaded yet.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}'''

# --- PHARMACY ---
templates['pharmacy/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Pharmacy Dashboard{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-pills text-primary me-2"></i> Pharmacy Dashboard</h2>
<div class="row">
    <div class="col-md-6 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-warning">{{ stats.pending_prescriptions }}</h1>
            <p class="text-muted fw-medium mb-3">Pending Prescriptions</p>
            <a href="/pharmacy/prescriptions" class="btn btn-outline-warning rounded-pill text-dark">View & Fulfill</a>
        </div>
    </div>
</div>
{% endblock %}'''

templates['pharmacy/view_prescriptions.html'] = '''{% extends "base.html" %}
{% block title %}Patient Prescriptions{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4">Patient Prescriptions</h2>
<div class="row">
    {% for pres in prescriptions %}
    <div class="col-md-6 mb-4">
        <div class="glass-card p-4 h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                    <h5 class="fw-bold mb-1">Patient #{{ pres.patient_id }}</h5>
                    <small class="text-muted">Issued by Hospital #{{ pres.hospital_id }} on {{ pres.created_at }}</small>
                </div>
                <span class="badge bg-{{ 'success' if pres.status == 'fulfilled' else 'warning text-dark' }} px-3 py-2 rounded-pill">
                    {{ pres.status|upper }}
                </span>
            </div>
            
            <div class="bg-light p-3 rounded-3 border mb-3">
                <p class="mb-2 fw-medium text-primary">Medicines:</p>
                <p class="mb-0" style="white-space: pre-line;">{{ pres.medicines }}</p>
            </div>
            
            <div class="row mb-3 small">
                <div class="col-6"><strong>Dosage:</strong> {{ pres.dosage }}</div>
                <div class="col-6"><strong>Duration:</strong> {{ pres.duration }}</div>
            </div>
            
            {% if pres.notes %}
            <p class="small text-muted mb-3"><strong>Notes:</strong> {{ pres.notes }}</p>
            {% endif %}
            
            {% if pres.status == 'pending' %}
            <form action="/pharmacy/fulfill-prescription/{{ pres.id }}" method="POST">
                <button type="submit" class="btn btn-success w-100 rounded-pill"><i class="fas fa-check-circle me-2"></i> Mark as Fulfilled</button>
            </form>
            {% else %}
            <button class="btn btn-secondary w-100 rounded-pill" disabled><i class="fas fa-check-double me-2"></i> Already Fulfilled</button>
            {% endif %}
        </div>
    </div>
    {% else %}
    <div class="col-12 text-center text-muted py-5">
        <i class="fas fa-prescription-bottle fa-3x mb-3 text-light"></i>
        <p>No pending prescriptions.</p>
    </div>
    {% endfor %}
</div>
{% endblock %}'''

# --- ERRORS ---
def get_error_html(code, title, desc):
    return f'''{{% extends "base.html" %}}
{{% block content %}}
<div class="text-center py-5">
    <h1 class="display-1 fw-bold text-primary">{code}</h1>
    <h3 class="fw-medium mb-3">{title}</h3>
    <p class="text-muted mb-4">{desc}</p>
    <a href="/" class="btn btn-primary rounded-pill px-4">Back to Home</a>
</div>
{{% endblock %}}'''

templates['errors/404.html'] = get_error_html("404", "Page Not Found", "The page you are looking for doesn't exist.")
templates['errors/403.html'] = get_error_html("403", "Access Denied", "You don't have permission to view this page.")
templates['errors/500.html'] = get_error_html("500", "Server Error", "Something went wrong on our end. Please try again.")

for filepath, content in templates.items():
    full_path = os.path.join(templates_dir, os.path.normpath(filepath))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
