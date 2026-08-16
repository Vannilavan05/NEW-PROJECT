# Secure Integrated Healthcare Management System (SIHMS)

![SIHMS Banner](https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&h=400&q=80)

SIHMS is a modern, unified web platform designed to seamlessly connect all pillars of healthcare—Patients, Hospitals, Scan Centres, and Pharmacies. By leveraging unique QR codes and a highly secure role-based architecture, SIHMS ensures that medical records, prescriptions, and scans are instantly accessible to the right people, precisely when they need it.

## 🚀 Key Features

### 👤 For Patients
*   **Unique Medical Identity:** Generate a dynamic QR code linked to your comprehensive medical profile.
*   **Access Control:** Review and approve/reject data access requests from external hospitals.
*   **Unified History:** View your entire medical history (prescriptions, scan reports) in one clean, glassmorphic dashboard.

### 🏥 For Hospitals
*   **Instant Access:** Scan a patient's QR code or enter their ID to instantly pull up their medical records.
*   **Digital Prescriptions:** Issue prescriptions that are directly tied to a patient's profile.
*   **Smart Pharmacy Search:** While writing a prescription, dynamically search all registered pharmacies in real-time to ensure the medicine is in stock before prescribing it.

### 🧪 For Scan Centres
*   **Seamless Uploads:** Search for a patient and directly upload their X-Rays, MRIs, and Blood Test reports to their digital profile.

### 💊 For Pharmacies
*   **Inventory Management:** Update tablet and medicine stock levels which dynamically populate the Hospital's search portal.
*   **Digital Fulfillment:** View pending prescriptions and mark them as fulfilled in real-time.

## 💻 Tech Stack
*   **Backend:** Python 3, Flask
*   **Database:** SQLite (Migrated from MySQL for zero-configuration local deployment)
*   **Frontend:** HTML5, CSS3, Bootstrap 5
*   **UI/UX Design:** Custom Glassmorphism aesthetic, Inter typography, CSS micro-animations.
*   **Integrations:** Python `qrcode`, `Pillow` for dynamic image generation.

## 🛠️ Local Setup & Installation

Follow these steps to run the application on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/Vannilavan05/SIHMS.git
cd SIHMS
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install flask qrcode pillow
```
*(Note: `flask-mysqldb` and `pymysql` are no longer required as the project has been fully migrated to SQLite for ease of use).*

### 3. Run the Server
Simply execute the main application file. The database (`database.db`) will automatically initialize itself on first run.
```bash
python app.py
```

### 4. Access the Application
Open your web browser and navigate to:
**http://127.0.0.1:5000**

## 🧪 Default Test Accounts
If the database is freshly initialized, you can use the included `seed_users.py` script to inject test data, or register new accounts from the UI. 

Sample test credentials (Password for all: `password123`):
- **Hospital:** `hospital1`
- **Patient:** `patient1`
- **Scan Centre:** `scan1`
- **Pharmacy:** `pharmacy1`

---
*Designed with a focus on premium aesthetics and frictionless user experiences.*