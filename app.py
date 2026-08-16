"""
Secure Integrated Healthcare Management System (SIHMS)
Main Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import qrcode
import io
import os
from datetime import datetime
import json
from flask import jsonify

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'sihms_secret_key_2026'

# SQLite Configuration
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


# ============================================================================
# DECORATORS & HELPER FUNCTIONS
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session:
                flash('Please log in first', 'warning')
                return redirect(url_for('login'))
            if session['role'] != role:
                flash('Unauthorized access', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_audit(user_id, action, entity_type, entity_id):
    """Log user actions for audit trail"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, timestamp)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, action, entity_type, entity_id))
        conn.commit()
    except Exception as e:
        print(f"Audit logging error: {e}")

def generate_qr_code(data):
    """Generate QR code for patient"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            log_audit(user['id'], 'LOGIN', 'user', user['id'])
            
            # Redirect based on role
            if user['role'] == 'hospital':
                return redirect(url_for('hospital_dashboard'))
            elif user['role'] == 'scan_centre':
                return redirect(url_for('scan_centre_dashboard'))
            elif user['role'] == 'patient':
                return redirect(url_for('patient_dashboard'))
            elif user['role'] == 'pharmacy':
                return redirect(url_for('pharmacy_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        organization = request.form.get('organization', '')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute("""
                INSERT INTO users (username, password, role, organization, created_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (username, hashed_password, role, organization))
            conn.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    if 'id' in session:
        log_audit(session['id'], 'LOGOUT', 'user', session['id'])
    
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# ============================================================================
# HOSPITAL ROUTES
# ============================================================================

@app.route('/hospital/dashboard')
@login_required
@role_required('hospital')
def hospital_dashboard():
    """Hospital dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get stats
    cursor.execute('SELECT COUNT(*) as count FROM approvals WHERE hospital_id = ? AND status = "approved"', 
                   (session['id'],))
    approved_patients = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM approvals WHERE hospital_id = ? AND status = "pending"', 
                   (session['id'],))
    pending_approvals = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM prescriptions WHERE hospital_id = ?', 
                   (session['id'],))
    prescriptions_count = cursor.fetchone()['count']

    stats = {
        'approved_patients': approved_patients,
        'pending_approvals': pending_approvals,
        'prescriptions': prescriptions_count
    }

    return render_template('hospital/dashboard.html', stats=stats)

@app.route('/hospital/request-access', methods=['GET', 'POST'])
@login_required
@role_required('hospital')
def hospital_request_access():
    """Hospital requests access to patient records"""
    if request.method == 'POST':
        patient_id_or_qr = request.form['patient_id_or_qr']

        conn = get_db()
        cursor = conn.cursor()
        
        # Search by ID or QR code
        cursor.execute("""
            SELECT id FROM patients WHERE id = ? OR qr_code = ? LIMIT 1
        """, (patient_id_or_qr, patient_id_or_qr))
        
        patient = cursor.fetchone()

        if not patient:
            flash('Patient not found', 'danger')
        else:
            patient_id = patient['id']
            
            # Check if approval already exists
            cursor.execute("""
                SELECT * FROM approvals WHERE patient_id = ? AND hospital_id = ?
            """, (patient_id, session['id']))
            
            existing = cursor.fetchone()

            if existing:
                flash('You already have a request for this patient', 'warning')
            else:
                # Create approval request
                cursor.execute("""
                    INSERT INTO approvals (patient_id, hospital_id, status, requested_at)
                    VALUES (?, ?, 'pending', CURRENT_TIMESTAMP)
                """, (patient_id, session['id']))
                conn.commit()

                log_audit(session['id'], 'REQUEST_ACCESS', 'patient', patient_id)
                flash('Access request sent to patient', 'success')

    return render_template('hospital/request_access.html')

@app.route('/hospital/patients')
@login_required
@role_required('hospital')
def hospital_view_patients():
    """View approved patients for hospital"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT p.* FROM patients p
        INNER JOIN approvals a ON p.id = a.patient_id
        WHERE a.hospital_id = ? AND a.status = 'approved'
        ORDER BY p.created_at DESC
    """, (session['id'],))
    
    patients = cursor.fetchall()

    return render_template('hospital/view_patients.html', patients=patients)

@app.route('/hospital/patient/<int:patient_id>')
@login_required
@role_required('hospital')
def hospital_patient_records(patient_id):
    """View specific patient's records"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check approval
    cursor.execute("""
        SELECT * FROM approvals WHERE patient_id = ? AND hospital_id = ? AND status = 'approved'
    """, (patient_id, session['id']))
    
    if not cursor.fetchone():
        flash('Access denied', 'danger')
        return redirect(url_for('hospital_view_patients'))

    # Get patient info
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()

    # Get records
    cursor.execute('SELECT * FROM records WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
    records = cursor.fetchall()

    # Get scans
    cursor.execute('SELECT * FROM scans WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
    scans = cursor.fetchall()

    return render_template('hospital/patient_records.html', patient=patient, records=records, scans=scans)

@app.route('/hospital/upload-prescription/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@role_required('hospital')
def hospital_upload_prescription(patient_id):
    """Upload prescription for patient"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Verify access
    cursor.execute("""
        SELECT * FROM approvals WHERE patient_id = ? AND hospital_id = ? AND status = 'approved'
    """, (patient_id, session['id']))
    
    if not cursor.fetchone():
        flash('Access denied', 'danger')
        return redirect(url_for('hospital_view_patients'))

    if request.method == 'POST':
        medicines = request.form['medicines']
        dosage = request.form['dosage']
        duration = request.form['duration']
        notes = request.form.get('notes', '')

        cursor.execute("""
            INSERT INTO prescriptions (patient_id, hospital_id, medicines, dosage, duration, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (patient_id, session['id'], medicines, dosage, duration, notes))
        conn.commit()

        log_audit(session['id'], 'UPLOAD_PRESCRIPTION', 'prescription', patient_id)
        flash('Prescription uploaded successfully', 'success')
        return redirect(url_for('hospital_patient_records', patient_id=patient_id))

    return render_template('hospital/upload_prescription.html', patient_id=patient_id)

# ============================================================================
# SCAN CENTRE ROUTES
# ============================================================================

@app.route('/scan-centre/dashboard')
@login_required
@role_required('scan_centre')
def scan_centre_dashboard():
    """Scan centre dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM scans WHERE scan_center_id = ?', (session['id'],))
    total_scans = cursor.fetchone()['count']

    stats = {'total_scans': total_scans}

    return render_template('scan_centre/dashboard.html', stats=stats)

@app.route('/scan-centre/upload-report', methods=['GET', 'POST'])
@login_required
@role_required('scan_centre')
def scan_centre_upload_report():
    """Upload scan report"""
    if request.method == 'POST':
        patient_id_or_qr = request.form['patient_id_or_qr']
        scan_type = request.form['scan_type']
        diagnosis = request.form.get('diagnosis', '')
        
        file = request.files['report_file']

        conn = get_db()
        cursor = conn.cursor()
        
        # Find patient
        cursor.execute("""
            SELECT id FROM patients WHERE id = ? OR qr_code = ? LIMIT 1
        """, (patient_id_or_qr, patient_id_or_qr))
        
        patient = cursor.fetchone()

        if not patient:
            flash('Patient not found', 'danger')
        elif not file or file.filename == '':
            flash('No file selected', 'danger')
        elif not allowed_file(file.filename):
            flash('Invalid file type. Allowed: PDF, JPG, PNG, GIF, DOC, DOCX', 'danger')
        else:
            # Save file
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save to database
            cursor.execute("""
                INSERT INTO scans (patient_id, scan_center_id, scan_type, report_path, diagnosis, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (patient['id'], session['id'], scan_type, filename, diagnosis))
            conn.commit()

            log_audit(session['id'], 'UPLOAD_SCAN', 'scan', patient['id'])
            flash('Scan report uploaded successfully', 'success')
            return redirect(url_for('scan_centre_dashboard'))

    return render_template('scan_centre/upload_report.html')

@app.route('/scan-centre/reports')
@login_required
@role_required('scan_centre')
def scan_centre_view_reports():
    """View uploaded reports"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM scans WHERE scan_center_id = ? ORDER BY created_at DESC
    """, (session['id'],))
    
    scans = cursor.fetchall()

    return render_template('scan_centre/view_reports.html', scans=scans)

# ============================================================================
# PATIENT ROUTES
# ============================================================================

@app.route('/patient/dashboard')
@login_required
@role_required('patient')
def patient_dashboard():
    """Patient dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get patient profile
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    patient = cursor.fetchone()

    if not patient:
        return redirect(url_for('patient_create_profile'))

    # Get stats
    cursor.execute('SELECT COUNT(*) as count FROM records WHERE patient_id = ?', (patient['id'],))
    total_records = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM scans WHERE patient_id = ?', (patient['id'],))
    total_scans = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM approvals WHERE patient_id = ? AND status = "pending"', (patient['id'],))
    pending_approvals = cursor.fetchone()['count']

    stats = {
        'total_records': total_records,
        'total_scans': total_scans,
        'pending_approvals': pending_approvals
    }

    return render_template('patient/dashboard.html', stats=stats, patient=patient)

@app.route('/patient/create-profile', methods=['GET', 'POST'])
@login_required
@role_required('patient')
def patient_create_profile():
    """Create patient profile"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if profile already exists
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    if cursor.fetchone():
        return redirect(url_for('patient_dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')

        # Generate QR code
        qr_data = f"SIHMS_{session['id']}_{datetime.now().timestamp()}"

        cursor.execute("""
            INSERT INTO patients (owner_user_id, name, age, blood_group, phone, address, qr_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (session['id'], name, age, blood_group, phone, address, qr_data))
        conn.commit()

        log_audit(session['id'], 'CREATE_PROFILE', 'patient', session['id'])
        flash('Profile created successfully', 'success')
        return redirect(url_for('patient_dashboard'))

    return render_template('patient/create_profile.html')

@app.route('/patient/records')
@login_required
@role_required('patient')
def patient_view_records():
    """View all patient records"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    patient = cursor.fetchone()

    if not patient:
        flash('Please create your profile first', 'warning')
        return redirect(url_for('patient_create_profile'))

    # Get all records
    cursor.execute('SELECT * FROM records WHERE patient_id = ? ORDER BY created_at DESC', (patient['id'],))
    records = cursor.fetchall()

    # Get all scans
    cursor.execute('SELECT * FROM scans WHERE patient_id = ? ORDER BY created_at DESC', (patient['id'],))
    scans = cursor.fetchall()

    # Get prescriptions
    cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ? ORDER BY created_at DESC', (patient['id'],))
    prescriptions = cursor.fetchall()

    return render_template('patient/view_records.html', patient=patient, records=records, scans=scans, prescriptions=prescriptions)

@app.route('/patient/approvals')
@login_required
@role_required('patient')
def patient_manage_approvals():
    """Manage access approvals"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    patient = cursor.fetchone()

    if not patient:
        flash('Please create your profile first', 'warning')
        return redirect(url_for('patient_create_profile'))

    # Get pending approvals
    cursor.execute("""
        SELECT a.*, u.organization FROM approvals a
        JOIN users u ON a.hospital_id = u.id
        WHERE a.patient_id = ?
        ORDER BY a.requested_at DESC
    """, (patient['id'],))
    
    approvals = cursor.fetchall()

    return render_template('patient/manage_approvals.html', approvals=approvals)

@app.route('/patient/approval/<int:approval_id>/<action>', methods=['POST'])
@login_required
@role_required('patient')
def patient_update_approval(approval_id, action):
    """Approve or reject hospital access"""
    if action not in ['approve', 'reject']:
        flash('Invalid action', 'danger')
        return redirect(url_for('patient_manage_approvals'))

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM approvals WHERE id = ?', (approval_id,))
    approval = cursor.fetchone()

    if not approval:
        flash('Approval not found', 'danger')
        return redirect(url_for('patient_manage_approvals'))

    # Verify ownership
    cursor.execute('SELECT * FROM patients WHERE id = ? AND owner_user_id = ?', 
                   (approval['patient_id'], session['id']))
    
    if not cursor.fetchone():
        flash('Unauthorized', 'danger')
        return redirect(url_for('patient_manage_approvals'))

    status = 'approved' if action == 'approve' else 'rejected'
    cursor.execute("""
        UPDATE approvals SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (status, approval_id))
    conn.commit()

    log_audit(session['id'], f'APPROVAL_{status.upper()}', 'approval', approval_id)
    flash(f'Request {status}', 'success')

    return redirect(url_for('patient_manage_approvals'))

@app.route('/patient/qr-code')
@login_required
@role_required('patient')
def patient_qr_code():
    """Generate and display patient QR code"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    patient = cursor.fetchone()

    if not patient:
        flash('Please create your profile first', 'warning')
        return redirect(url_for('patient_create_profile'))

    qr_img = generate_qr_code(patient['qr_code'])
    
    # Save to bytes
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/patient/download-records')
@login_required
@role_required('patient')
def patient_download_records():
    """Download patient records as PDF/JSON"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE owner_user_id = ?', (session['id'],))
    patient = cursor.fetchone()

    if not patient:
        flash('Please create your profile first', 'warning')
        return redirect(url_for('patient_create_profile'))

    # Get all data
    cursor.execute('SELECT * FROM records WHERE patient_id = ?', (patient['id'],))
    records = cursor.fetchall()

    cursor.execute('SELECT * FROM scans WHERE patient_id = ?', (patient['id'],))
    scans = cursor.fetchall()

    cursor.execute('SELECT * FROM prescriptions WHERE patient_id = ?', (patient['id'],))
    prescriptions = cursor.fetchall()

    # Create JSON export
    export_data = {
        'patient': patient,
        'records': records,
        'scans': scans,
        'prescriptions': prescriptions
    }

    # Convert to proper format for JSON
    export_json = json.dumps(export_data, default=str, indent=2)

    return send_file(
        io.BytesIO(export_json.encode()),
        mimetype='application/json',
        as_attachment=True,
        download_name=f"patient_records_{patient['id']}.json"
    )

# ============================================================================
# PHARMACY ROUTES
# ============================================================================

@app.route('/pharmacy/dashboard')
@login_required
@role_required('pharmacy')
def pharmacy_dashboard():
    """Pharmacy dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) as count FROM prescriptions 
        WHERE status = 'pending'
    """)
    pending_prescriptions = cursor.fetchone()['count']

    stats = {'pending_prescriptions': pending_prescriptions}

    return render_template('pharmacy/dashboard.html', stats=stats)

@app.route('/pharmacy/prescriptions')
@login_required
@role_required('pharmacy')
def pharmacy_view_prescriptions():
    """View all prescriptions"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, pat.name as patient_name FROM prescriptions p
        JOIN patients pat ON p.patient_id = pat.id
        ORDER BY p.created_at DESC
    """)
    
    prescriptions = cursor.fetchall()

    return render_template('pharmacy/view_prescriptions.html', prescriptions=prescriptions)

@app.route('/pharmacy/prescription/<int:prescription_id>/update-status', methods=['POST'])
@login_required
@role_required('pharmacy')
def pharmacy_update_status(prescription_id):
    """Update prescription fulfillment status"""
    status = request.form['status']

    if status not in ['pending', 'fulfilled', 'cancelled']:
        flash('Invalid status', 'danger')
        return redirect(url_for('pharmacy_view_prescriptions'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE prescriptions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (status, prescription_id))
    conn.commit()

    log_audit(session['id'], 'UPDATE_PRESCRIPTION_STATUS', 'prescription', prescription_id)
    flash(f'Prescription status updated to {status}', 'success')

    return redirect(url_for('pharmacy_view_prescriptions'))

# ============================================================================
# FILE DOWNLOAD
# ============================================================================

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Download uploaded file"""
    filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        flash('File not found', 'danger')
        return redirect(url_for('index'))

    return send_file(filepath, as_attachment=True)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

# ============================================================================
# NEW FEATURES: INVENTORY & SEARCH
# ============================================================================

@app.route('/scan_centre/search-patient', methods=['GET', 'POST'])
@login_required
@role_required('scan_centre')
def scan_centre_search_patient():
    """Scan Centre searches for a patient before uploading"""
    if request.method == 'POST':
        patient_id_or_qr = request.form.get('patient_id_or_qr', '')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ? OR qr_code = ? LIMIT 1", (patient_id_or_qr, patient_id_or_qr))
        patient = cursor.fetchone()
        
        if patient:
            return render_template('scan_centre/search_patient.html', patient=patient, query=patient_id_or_qr)
        else:
            flash('Patient not found.', 'danger')
            return render_template('scan_centre/search_patient.html', error=True)
            
    return render_template('scan_centre/search_patient.html')

@app.route('/pharmacy/inventory', methods=['GET', 'POST'])
@login_required
@role_required('pharmacy')
def pharmacy_inventory():
    """Pharmacy manages their medicine inventory"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        medicine_name = request.form.get('medicine_name', '').strip()
        stock_quantity = request.form.get('stock_quantity', 0)
        
        if medicine_name and int(stock_quantity) >= 0:
            try:
                cursor.execute("""
                    INSERT INTO pharmacy_inventory (pharmacy_id, medicine_name, stock_quantity)
                    VALUES (?, ?, ?)
                    ON CONFLICT(pharmacy_id, medicine_name) DO UPDATE SET
                    stock_quantity = ?, last_updated = CURRENT_TIMESTAMP
                """, (session['id'], medicine_name, stock_quantity, stock_quantity))
                conn.commit()
                flash(f'Updated stock for {medicine_name}', 'success')
            except Exception as e:
                flash(f'Error updating stock: {e}', 'danger')
        else:
            flash('Invalid medicine name or quantity.', 'danger')
            
        return redirect(url_for('pharmacy_inventory'))
        
    cursor.execute("SELECT * FROM pharmacy_inventory WHERE pharmacy_id = ? ORDER BY medicine_name ASC", (session['id'],))
    inventory = cursor.fetchall()
    
    return render_template('pharmacy/inventory.html', inventory=inventory)

@app.route('/hospital/search-pharmacy', methods=['GET'])
@login_required
@role_required('hospital')
def hospital_search_pharmacy():
    """AJAX endpoint for hospitals to search for medicine availability"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username as pharmacy_name, pi.medicine_name, pi.stock_quantity, pi.last_updated
        FROM pharmacy_inventory pi
        JOIN users u ON pi.pharmacy_id = u.id
        WHERE pi.medicine_name LIKE ? AND pi.stock_quantity > 0
        ORDER BY pi.stock_quantity DESC
        LIMIT 20
    """, ('%' + query + '%',))
    
    results = [dict(row) for row in cursor.fetchall()]
    return jsonify(results)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
