========================================================================
                  MEDICAL STORE MANAGEMENT SYSTEM
========================================================================

This is a Django-based Medical Store Management System application.
It manages medicines, stock, sales, billing, H1 drugs, bookings, and
general store inventory.

------------------------------------------------------------------------
PREREQUISITES
------------------------------------------------------------------------
- Python 3.10+ (tested with Python 3.13)
- pip (Python package manager)

------------------------------------------------------------------------
HOW TO RUN THE PROJECT
------------------------------------------------------------------------

1. (RECOMMENDED) Set Up a Virtual Environment:
   Open PowerShell in this project folder and run:

       python -m venv venv
       .\venv\Scripts\Activate.ps1

2. Install Dependencies:
   Install all required packages from requirements.txt:

       pip install -r requirements.txt

   Required packages include:
   - Django
   - Pillow (required for image fields)
   - asgiref
   - sqlparse
   - tzdata

3. Apply Database Migrations:
   Initialize or update the SQLite database (db.sqlite3):

       python manage.py migrate

4. Create an Admin / Superuser Account (Optional):
   To create your own admin login:

       python manage.py createsuperuser

   Follow the prompts to enter a username, email, and password.

5. Start the Development Server:
   Run the following command to start Django:

       python manage.py runserver

6. Open in Browser:
   Navigate to the following URLs in your web browser:

   - Home / Dashboard : http://127.0.0.1:8000/
   - Login Page       : http://127.0.0.1:8000/login/
   - Django Admin     : http://127.0.0.1:8000/admin/

------------------------------------------------------------------------
PROJECT FEATURES
------------------------------------------------------------------------
- Dashboard: Overview of medicines, sales, bills, and low stock warnings
- Medicines: Add, search, and manage medicine inventory with image uploads
- Sales & Billing: Record sales and generate printable bills
- Member Bills: Medical bills grouped by member / customer
- H1 Drugs: Schedule H1 drug register and compliance tracking
- General Store: Separate inventory, sales, and billing for general items
- Medicine Booking: Customer pre-booking management and status updates

========================================================================

