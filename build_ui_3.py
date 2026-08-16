import os

templates_dir = r'c:\Users\vanni\Downloads\NEW-PROJECT-main\NEW-PROJECT-main\templates'
templates = {}

# --- SCAN CENTRE ---
templates['scan_centre/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Scan Centre Dashboard{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-x-ray text-primary me-2"></i> Scan Centre Dashboard</h2>
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center">
            <h1 class="display-4 fw-bold text-info">{{ stats.total_scans }}</h1>
            <p class="text-muted fw-medium mb-3">Total Scans Uploaded</p>
            <a href="/scan_centre/reports" class="btn btn-outline-info rounded-pill">View All Uploads</a>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column justify-content-center">
            <h4 class="fw-bold">Search Patient</h4>
            <p class="text-muted small">Find a patient via QR or ID before uploading a report.</p>
            <a href="/scan_centre/search-patient" class="btn btn-primary rounded-pill mt-2">Search Patient</a>
        </div>
    </div>
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column justify-content-center border-primary" style="border: 2px dashed var(--primary);">
            <i class="fas fa-cloud-upload-alt fa-2x text-primary mb-2"></i>
            <h4 class="fw-bold">Upload Report</h4>
            <a href="/scan_centre/upload-report" class="btn btn-primary rounded-pill mt-2">Upload Now</a>
        </div>
    </div>
</div>
{% endblock %}'''

templates['scan_centre/search_patient.html'] = '''{% extends "base.html" %}
{% block title %}Search Patient{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="glass-card p-4 mb-4">
            <h3 class="fw-bold mb-3">Search Patient</h3>
            <form method="POST" class="d-flex gap-2">
                <input type="text" class="form-control form-control-lg" name="patient_id_or_qr" required placeholder="Enter Patient ID or scan QR code" value="{{ query if query else '' }}">
                <button type="submit" class="btn btn-primary px-4 rounded-pill"><i class="fas fa-search"></i></button>
            </form>
        </div>

        {% if patient %}
        <div class="glass-card p-4 border-start border-4 border-success">
            <h4 class="fw-bold text-success mb-3"><i class="fas fa-check-circle me-2"></i> Patient Found</h4>
            <div class="row mb-4">
                <div class="col-md-6">
                    <p class="mb-1"><strong>Name:</strong> {{ patient.name }}</p>
                    <p class="mb-1"><strong>ID:</strong> #{{ patient.id }}</p>
                    <p class="mb-1"><strong>Age:</strong> {{ patient.age }}</p>
                </div>
                <div class="col-md-6">
                    <p class="mb-1"><strong>Blood Group:</strong> <span class="badge bg-danger">{{ patient.blood_group }}</span></p>
                    <p class="mb-1"><strong>Phone:</strong> {{ patient.phone }}</p>
                </div>
            </div>
            <a href="/scan_centre/upload-report?patient_id={{ patient.id }}" class="btn btn-success w-100 py-2 rounded-pill">
                <i class="fas fa-file-upload me-2"></i> Upload Scan for this Patient
            </a>
        </div>
        {% endif %}
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
                    <input type="text" class="form-control" name="patient_id_or_qr" required placeholder="e.g. SIHMS_12_168..." value="{{ request.args.get('patient_id', '') }}">
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

# --- PHARMACY ---
templates['pharmacy/dashboard.html'] = '''{% extends "base.html" %}
{% block title %}Pharmacy Dashboard{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-pills text-primary me-2"></i> Pharmacy Dashboard</h2>
<div class="row">
    <div class="col-md-6 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column justify-content-center">
            <h1 class="display-4 fw-bold text-warning">{{ stats.pending_prescriptions }}</h1>
            <p class="text-muted fw-medium mb-3">Pending Prescriptions</p>
            <a href="/pharmacy/prescriptions" class="btn btn-outline-warning rounded-pill text-dark">View & Fulfill</a>
        </div>
    </div>
    <div class="col-md-6 mb-4">
        <div class="glass-card p-4 text-center h-100 d-flex flex-column justify-content-center border-success" style="border: 2px dashed var(--bs-success);">
            <i class="fas fa-boxes fa-3x text-success mb-3"></i>
            <h4 class="fw-bold">Manage Inventory</h4>
            <p class="text-muted small">Update your medicine stock levels so hospitals can find them.</p>
            <a href="/pharmacy/inventory" class="btn btn-success rounded-pill mt-2">Open Inventory</a>
        </div>
    </div>
</div>
{% endblock %}'''

templates['pharmacy/inventory.html'] = '''{% extends "base.html" %}
{% block title %}Pharmacy Inventory{% endblock %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="fas fa-boxes text-success me-2"></i> Manage Inventory</h2>
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="glass-card p-4">
            <h5 class="fw-bold mb-3">Update Stock</h5>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label fw-medium">Medicine Name</label>
                    <input type="text" class="form-control" name="medicine_name" required placeholder="e.g. Paracetamol 500mg">
                </div>
                <div class="mb-3">
                    <label class="form-label fw-medium">Quantity (Tablets)</label>
                    <input type="number" class="form-control" name="stock_quantity" min="0" required value="0">
                </div>
                <button type="submit" class="btn btn-success w-100 rounded-pill"><i class="fas fa-save me-2"></i> Save / Update</button>
            </form>
        </div>
    </div>
    <div class="col-md-8">
        <div class="glass-card p-4">
            <h5 class="fw-bold mb-3">Current Stock</h5>
            <div class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead class="table-light">
                        <tr>
                            <th>Medicine</th>
                            <th>Stock Quantity</th>
                            <th>Last Updated</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in inventory %}
                        <tr>
                            <td class="fw-bold text-primary">{{ item.medicine_name }}</td>
                            <td>
                                <span class="badge bg-{{ 'success' if item.stock_quantity > 50 else 'warning text-dark' if item.stock_quantity > 0 else 'danger' }} rounded-pill px-3">
                                    {{ item.stock_quantity }}
                                </span>
                            </td>
                            <td class="text-muted small">{{ item.last_updated }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="3" class="text-center py-4 text-muted">No medicines in inventory yet.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# --- HOSPITAL ---
templates['hospital/upload_prescription.html'] = '''{% extends "base.html" %}
{% block title %}Issue Prescription{% endblock %}
{% block content %}
<div class="row">
    <!-- Prescription Form (Left) -->
    <div class="col-md-7 mb-4">
        <div class="glass-card p-4 h-100">
            <h3 class="fw-bold mb-4">Issue Prescription</h3>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label fw-medium">Medicines (One per line)</label>
                    <textarea class="form-control" name="medicines" id="medicinesArea" rows="4" required></textarea>
                    <small class="text-muted">Use the search panel to find available medicines and click "+" to add them here.</small>
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
                <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill"><i class="fas fa-file-prescription me-2"></i> Submit Prescription</button>
            </form>
        </div>
    </div>

    <!-- Pharmacy Search (Right) -->
    <div class="col-md-5 mb-4">
        <div class="glass-card p-4 h-100 bg-primary bg-opacity-10 border-primary">
            <h4 class="fw-bold text-primary mb-3"><i class="fas fa-search-location me-2"></i> Find Medicines</h4>
            <p class="text-muted small">Search pharmacy inventories in real-time before prescribing.</p>
            
            <div class="input-group mb-4">
                <input type="text" class="form-control" id="pharmacySearchInput" placeholder="Search medicine name...">
                <button class="btn btn-primary" type="button" onclick="searchPharmacy()"><i class="fas fa-search"></i></button>
            </div>

            <div id="searchResults" class="list-group" style="max-height: 400px; overflow-y: auto;">
                <div class="text-center text-muted py-4" id="searchPlaceholder">
                    Type a medicine name to check availability across pharmacies.
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function searchPharmacy() {
        const query = document.getElementById('pharmacySearchInput').value;
        const resultsContainer = document.getElementById('searchResults');
        
        if(query.trim() === '') {
            resultsContainer.innerHTML = '<div class="text-center text-muted py-4">Type a medicine name...</div>';
            return;
        }
        
        resultsContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"></div></div>';
        
        fetch(`/hospital/search-pharmacy?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                if(data.length === 0) {
                    resultsContainer.innerHTML = '<div class="text-center text-danger py-4"><i class="fas fa-exclamation-circle mb-2"></i><br>Not found in any nearby pharmacy.</div>';
                    return;
                }
                
                let html = '';
                data.forEach(item => {
                    html += `
                        <div class="list-group-item list-group-item-action d-flex justify-content-between align-items-center mb-2 rounded-3 border-0 shadow-sm">
                            <div>
                                <h6 class="mb-1 fw-bold text-dark">${item.medicine_name}</h6>
                                <p class="mb-0 small text-muted"><i class="fas fa-store me-1"></i> ${item.pharmacy_name}</p>
                            </div>
                            <div class="text-end">
                                <span class="badge bg-success rounded-pill mb-1">${item.stock_quantity} in stock</span><br>
                                <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2 rounded-pill" onclick="addMedicine('${item.medicine_name}')"><i class="fas fa-plus"></i> Add</button>
                            </div>
                        </div>
                    `;
                });
                resultsContainer.innerHTML = html;
            });
    }

    function addMedicine(name) {
        const area = document.getElementById('medicinesArea');
        if(area.value) {
            area.value += '\\n' + name;
        } else {
            area.value = name;
        }
        // Visual feedback
        area.style.backgroundColor = '#d1e7dd';
        setTimeout(() => area.style.backgroundColor = '', 300);
    }
    
    document.getElementById('pharmacySearchInput').addEventListener('keypress', function(e) {
        if(e.key === 'Enter') {
            searchPharmacy();
        }
    });
</script>
{% endblock %}'''

for filepath, content in templates.items():
    full_path = os.path.join(templates_dir, os.path.normpath(filepath))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
