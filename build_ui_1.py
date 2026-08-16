import os

templates_dir = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\templates'

templates = {}

# --- HOSPITAL ---
templates['hospital/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Hospital Dashboard{% endblock %}
{% block content %}
<div class="page-header d-flex justify-content-between align-items-center">
    <h2 class="fw-bold"><i class="fas fa-hospital text-primary me-2"></i> Hospital Dashboard</h2>
</div>
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-primary">{{ stats.approved_patients }}</h1>
            <p class="text-muted fw-medium mb-0">Approved Patients</p>
            <a href="/hospital/patients" class="btn btn-sm btn-outline-primary mt-3 rounded-pill">View All</a>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-warning">{{ stats.pending_approvals }}</h1>
            <p class="text-muted fw-medium mb-0">Pending Requests</p>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-success">{{ stats.prescriptions }}</h1>
            <p class="text-muted fw-medium mb-0">Prescriptions Issued</p>
        </div>
    </div>
</div>
{% endblock %}'''

templates['hospital/request_access.html'] = '''{% extends "base.html" %}
{% block title %}Request Access{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="glass-card p-5">
            <h3 class="fw-bold mb-4 text-center">Request Patient Access</h3>
            <p class="text-muted text-center mb-4">Scan the patient's QR Code string or enter their Patient ID to request access to their medical records.</p>
            <form method="POST">
                <div class="mb-4">
                    <label class="form-label fw-medium">Patient ID or QR Code</label>
                    <input type="text" class="form-control form-control-lg" name="patient_id_or_qr" required placeholder="e.g., SIHMS_12_168...">
                </div>
                <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill"><i class="fas fa-paper-plane me-2"></i> Send Request</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}'''

templates['hospital/view_patients.html'] = '''{% extends "base.html" %}
{% block title %}Approved Patients{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-users text-primary me-2"></i> Approved Patients</h2>
<div class="glass-card p-4">
    <div class="table-responsive">
        <table class="table table-hover align-middle">
            <thead class="table-light">
                <tr>
                    <th>Patient ID</th>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Blood Group</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for p in patients %}
                <tr>
                    <td>#{{ p.id }}</td>
                    <td class="fw-medium">{{ p.name }}</td>
                    <td>{{ p.age }}</td>
                    <td><span class="badge bg-danger rounded-pill">{{ p.blood_group }}</span></td>
                    <td>
                        <a href="/hospital/patient/{{ p.id }}" class="btn btn-sm btn-primary rounded-pill px-3">View Records</a>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" class="text-center py-4 text-muted">No approved patients found.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}'''

templates['hospital/upload_prescription.html'] = '''{% extends "base.html" %}
{% block title %}Issue Prescription{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="glass-card p-4">
            <h3 class="fw-bold mb-4">Issue Prescription</h3>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label fw-medium">Medicines (One per line)</label>
                    <textarea class="form-control" name="medicines" rows="4" required></textarea>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-medium">Dosage</label>
                        <input type="text" class="form-control" name="dosage" placeholder="e.g. 1-0-1 after food">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-medium">Duration</label>
                        <input type="text" class="form-control" name="duration" placeholder="e.g. 5 days">
                    </div>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-medium">Additional Notes</label>
                    <textarea class="form-control" name="notes" rows="2"></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-2"><i class="fas fa-file-prescription me-2"></i> Submit Prescription</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}'''

templates['hospital/patient_records.html'] = '''{% extends "base.html" %}
{% block title %}Patient Records{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold">{{ patient.name }}'s Records</h2>
    <a href="/hospital/upload-prescription/{{ patient.id }}" class="btn btn-primary rounded-pill"><i class="fas fa-plus me-2"></i> New Prescription</a>
</div>

<div class="row">
    <div class="col-md-4">
        <div class="glass-card p-4 mb-4">
            <h5 class="fw-bold text-primary mb-3">Patient Info</h5>
            <ul class="list-unstyled mb-0">
                <li class="mb-2"><strong>ID:</strong> #{{ patient.id }}</li>
                <li class="mb-2"><strong>Age:</strong> {{ patient.age }}</li>
                <li class="mb-2"><strong>Blood:</strong> <span class="badge bg-danger">{{ patient.blood_group }}</span></li>
                <li class="mb-2"><strong>Phone:</strong> {{ patient.phone }}</li>
            </ul>
        </div>
    </div>
    <div class="col-md-8">
        <h4 class="fw-bold mb-3">Scans & Reports</h4>
        {% for scan in scans %}
        <div class="glass-card p-3 mb-3 border-start border-4 border-info">
            <div class="d-flex justify-content-between">
                <h5 class="mb-1 text-info">{{ scan.scan_type }}</h5>
                <small class="text-muted">{{ scan.created_at }}</small>
            </div>
            <p class="mb-0"><strong>Diagnosis:</strong> {{ scan.diagnosis }}</p>
        </div>
        {% else %}
        <p class="text-muted">No scan reports found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}'''

# --- PATIENT ---
templates['patient/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Patient Dashboard{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4">Welcome back, {{ session.username }}</h2>
{% if not patient %}
<div class="alert alert-warning shadow-sm border-0 rounded-4">
    <h4 class="alert-heading"><i class="fas fa-exclamation-triangle me-2"></i> Profile Incomplete</h4>
    <p>Please create your patient profile to generate your unique QR Code and start managing your health records.</p>
    <a href="/patient/create-profile" class="btn btn-warning rounded-pill mt-2">Create Profile Now</a>
</div>
{% else %}
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column align-items-center justify-content-center">
            <h5 class="fw-bold text-primary mb-3">Your Medical QR Code</h5>
            <div class="qr-container bg-white p-2 rounded-4 shadow-sm mb-3 d-inline-block">
                <img src="/patient/qr-code" alt="QR Code" class="img-fluid" style="width: 200px; height: 200px;">
            </div>
            <p class="small text-muted mb-0">Show this QR code to hospitals or scan centres to grant them access to your profile.</p>
        </div>
    </div>
    <div class="col-md-8 mb-4">
        <div class="row h-100">
            <div class="col-sm-6 mb-4">
                <div class="glass-card p-4 text-center h-100">
                    <h1 class="display-4 fw-bold text-info">{{ stats.total_records }}</h1>
                    <p class="text-muted fw-medium mb-0">Medical Records</p>
                </div>
            </div>
            <div class="col-sm-6 mb-4">
                <div class="glass-card p-4 text-center h-100">
                    <h1 class="display-4 fw-bold text-success">{{ stats.total_scans }}</h1>
                    <p class="text-muted fw-medium mb-0">Scan Reports</p>
                </div>
            </div>
            <div class="col-sm-12">
                <div class="glass-card p-4 text-center">
                    <h1 class="display-4 fw-bold text-warning">{{ stats.pending_approvals }}</h1>
                    <p class="text-muted fw-medium mb-3">Pending Access Requests</p>
                    <a href="/patient/manage-approvals" class="btn btn-outline-warning rounded-pill">Manage Requests</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}'''

templates['patient/create_profile.html'] = '''{% extends "base.html" %}
{% block title %}Create Profile{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="glass-card p-5">
            <h3 class="fw-bold mb-4 text-center">Patient Profile Details</h3>
            <form method="POST">
                <div class="row">
                    <div class="col-md-8 mb-3">
                        <label class="form-label fw-medium">Full Name</label>
                        <input type="text" class="form-control" name="name" required>
                    </div>
                    <div class="col-md-4 mb-3">
                        <label class="form-label fw-medium">Age</label>
                        <input type="number" class="form-control" name="age" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-medium">Blood Group</label>
                        <select class="form-select form-control" name="blood_group">
                            <option value="A+">A+</option><option value="A-">A-</option>
                            <option value="B+">B+</option><option value="B-">B-</option>
                            <option value="O+">O+</option><option value="O-">O-</option>
                            <option value="AB+">AB+</option><option value="AB-">AB-</option>
                        </select>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label fw-medium">Phone Number</label>
                        <input type="text" class="form-control" name="phone">
                    </div>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-medium">Address</label>
                    <textarea class="form-control" name="address" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-3 rounded-pill">Save Profile & Generate QR</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}'''

templates['patient/view_records.html'] = '''{% extends "base.html" %}
{% block title %}My Records{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4">My Medical History</h2>
<div class="row">
    <div class="col-md-6 mb-4">
        <h4 class="fw-bold mb-3"><i class="fas fa-file-prescription text-primary me-2"></i> Prescriptions</h4>
        {% for pres in prescriptions %}
        <div class="glass-card p-3 mb-3 border-start border-4 border-primary">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-{{ 'success' if pres.status == 'fulfilled' else 'warning text-dark' }}">{{ pres.status|title }}</span>
                <small class="text-muted">{{ pres.created_at }}</small>
            </div>
            <p class="mb-1"><strong>Medicines:</strong><br>{{ pres.medicines | replace('\n', '<br>') | safe }}</p>
            <p class="mb-0 small text-muted"><i class="fas fa-clock me-1"></i> {{ pres.duration }} | {{ pres.dosage }}</p>
        </div>
        {% else %}
        <div class="glass-card p-4 text-center text-muted">No prescriptions found.</div>
        {% endfor %}
    </div>
    <div class="col-md-6 mb-4">
        <h4 class="fw-bold mb-3"><i class="fas fa-x-ray text-info me-2"></i> Scans & Reports</h4>
        {% for scan in scans %}
        <div class="glass-card p-3 mb-3 border-start border-4 border-info">
            <h5 class="text-info mb-1">{{ scan.scan_type }}</h5>
            <small class="text-muted d-block mb-2">{{ scan.created_at }}</small>
            <p class="mb-0">{{ scan.diagnosis }}</p>
        </div>
        {% else %}
        <div class="glass-card p-4 text-center text-muted">No scan reports found.</div>
        {% endfor %}
    </div>
</div>
{% endblock %}'''

templates['patient/manage_approvals.html'] = '''{% extends "base.html" %}
{% block title %}Manage Approvals{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-shield-alt text-primary me-2"></i> Access Requests</h2>
<div class="glass-card p-4">
    <div class="table-responsive">
        <table class="table align-middle">
            <thead class="table-light">
                <tr>
                    <th>Date Requested</th>
                    <th>Hospital ID</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for a in approvals %}
                <tr>
                    <td>{{ a.requested_at }}</td>
                    <td class="fw-medium">Hospital #{{ a.hospital_id }}</td>
                    <td>
                        <span class="badge bg-{{ 'success' if a.status == 'approved' else 'warning text-dark' if a.status == 'pending' else 'danger' }}">
                            {{ a.status|title }}
                        </span>
                    </td>
                    <td>
                        {% if a.status == 'pending' %}
                        <div class="d-flex gap-2">
                            <form action="/patient/approve-access/{{ a.id }}" method="POST"><button type="submit" class="btn btn-sm btn-success rounded-pill px-3"><i class="fas fa-check me-1"></i> Approve</button></form>
                            <form action="/patient/reject-access/{{ a.id }}" method="POST"><button type="submit" class="btn btn-sm btn-danger rounded-pill px-3"><i class="fas fa-times me-1"></i> Reject</button></form>
                        </div>
                        {% else %}
                        <span class="text-muted small">Action Taken</span>
                        {% endif %}
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="4" class="text-center py-4 text-muted">No access requests.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}'''

for filepath, content in templates.items():
    full_path = os.path.join(templates_dir, os.path.normpath(filepath))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
