# NET BANKING - Banking Management System (Backend)

A complete, secure Python Flask & MySQL backend for the **NET BANKING Management System**.

## 🚀 Features

- **Authentication & Security**: Session-based login, register, password change, route security with `@login_required`.
- **Dashboard**: Real-time summary counts (Customers, Accounts, Deposits, Transactions) and recent activities.
- **Customer Management**: Add, Edit, Delete, Search, and View Customer details.
- **Account Management**: Auto-generate unique Account Numbers, Open/Close Accounts, Track Balances.
- **Deposit & Withdrawal**: Atomic financial operations with balance validation, receipt generation.
- **Fund Transfer**: Atomic double-entry transfer between sender & receiver with balance checks.
- **Balance Enquiry**: Instant account balance check.
- **Transaction History**: Comprehensive log with search filters.
- **Reports & Analytics**: Daily/Weekly/Monthly reports with PDF (ReportLab) & Excel (openpyxl) export capabilities.
- **System Settings & Profile**: Update Admin profile and system configurations dynamically.
- **Contact & About**: Dynamic about page and database persistence for contact form submissions.

---

## 🛠 Project Structure

```
BankManagementSystem/
├── app.py                  # Main Flask application entrypoint & blueprint registrations
├── config.py               # Application configurations (Database, Secret Key, Uploads)
├── db.py                   # MySQL connection pooling & parameterized execution helpers
├── requirements.txt        # Python package dependencies
├── README.md               # Documentation
│
├── database/
│   └── bank_management.sql # Database schema & sample data
│
├── models/                 # Database Query Layer
│   ├── admin_model.py
│   ├── customer_model.py
│   ├── account_model.py
│   ├── transaction_model.py
│   ├── report_model.py
│   ├── contact_model.py
│   └── settings_model.py
│
├── routes/                 # Flask Blueprints
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── customer_routes.py
│   ├── account_routes.py
│   ├── transaction_routes.py
│   ├── report_routes.py
│   └── main_routes.py
│
├── services/               # Core Business & Export Logic
│   ├── banking_service.py
│   └── export_service.py
│
├── utils/                  # Helpers & Security
│   ├── auth_decorator.py
│   ├── helpers.py
│   └── validators.py
│
├── static/                 # CSS, Images, JS
├── templates/              # Jinja2 HTML Templates
└── uploads/                # Exported PDF and Excel reports
```

---

## 📥 Setup & Installation

### 1. Database Setup (MySQL)
Open your MySQL client or MySQL Workbench and run:
```sql
SOURCE database/bank_management.sql;
```
Or import `database/bank_management.sql` directly into MySQL.

Default Database Credentials in `config.py`:
- **Database**: `bank_management`
- **Host**: `localhost`
- **User**: `root`
- **Password**: `raju`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Open `http://localhost:5000` in your web browser.

Default Admin Login:
- **Username**: `admin`
- **Password**: `admin123`
