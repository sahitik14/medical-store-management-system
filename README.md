# Medical Store Management System

A Django-based web application for managing a medical store and general store, including medicines, inventory, sales, billing, H1 drug compliance, and member tracking.

---

## Prerequisites

- **Python**: 3.10+ (tested with Python 3.13)
- **pip**: Package installer for Python

---

## How to Run the Project

### 1. (Recommended) Set Up a Virtual Environment

Open PowerShell in the project root directory and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

Install the required packages from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

> **Note**: `Pillow` is required for handling product and medicine image uploads.

### 3. Apply Migrations

Verify and apply database migrations to the SQLite database:

```powershell
python manage.py migrate
```

### 4. Create an Admin Account (Optional)

Create a superuser to access the Django administration panel:

```powershell
python manage.py createsuperuser
```

### 5. Run the Development Server

Start the local Django server:

```powershell
python manage.py runserver
```

### 6. Access the Application

Open your browser and visit:

- **Dashboard / Home**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) *(redirects to login)*
- **Login Page**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Features

- **Dashboard**: High-level store metrics and low stock alerts
- **Medicine Inventory**: Full CRUD for medicines with image support
- **Sales & Billing**: Record transactions and generate printable bills
- **H1 Drug Register**: Specialized tracking for Schedule H1 drug sales
- **General Store**: Separate management and billing for non-medical items
- **Medicine Booking**: Customer medicine pre-booking and status tracking
- **Member Bills**: Customer-wise transaction aggregation

