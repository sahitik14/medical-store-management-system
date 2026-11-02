from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Medicine,
    Sale,
    Bill,
    H1Drug,
    H1Sale,
    MedicineBooking,
)


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "login.html")


# =========================
# LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect("login")


# =========================
# HOME
# =========================

@login_required
def home(request):

    total_medicines = Medicine.objects.count()
    total_sales = Sale.objects.count()
    total_bills = Bill.objects.count()

    low_stock_medicines = Medicine.objects.filter(
        stock__lte=10
    )

    return render(request, "home.html", {
        "total_medicines": total_medicines,
        "total_sales": total_sales,
        "total_bills": total_bills,
        "low_stock": low_stock_medicines.count(),
        "low_stock_medicines": low_stock_medicines,
    })


# =========================
# MEDICINES
# =========================

@login_required
def medicines(request):

    search = request.GET.get("search", "")

    if search:
        medicine_list = Medicine.objects.filter(
            name__icontains=search
        )
    else:
        medicine_list = Medicine.objects.all()

    return render(request, "medicines.html", {
        "medicines": medicine_list,
        "search": search,
    })


# =========================
# NORMAL MEDICINE SALES
# =========================

@login_required
def sales(request):

    medicines_list = Medicine.objects.all()

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        medicine_id = request.POST.get("medicine")
        quantity_text = request.POST.get("quantity")

        if not quantity_text:
            return render(request, "sales.html", {
                "medicines": medicines_list,
                "error": "Please enter quantity."
            })

        try:
            quantity = int(quantity_text)
        except ValueError:
            return render(request, "sales.html", {
                "medicines": medicines_list,
                "error": "Invalid quantity."
            })

        medicine = Medicine.objects.get(id=medicine_id)

        if quantity <= 0:
            return render(request, "sales.html", {
                "medicines": medicines_list,
                "error": "Quantity must be greater than 0."
            })

        if quantity <= medicine.stock:

            total_price = medicine.price * quantity

            Sale.objects.create(
                customer_name=customer_name,
                medicine=medicine,
                quantity=quantity,
                total_price=total_price,
            )

            medicine.stock -= quantity
            medicine.save()

            bill = Bill.objects.create(
                customer_name=customer_name,
                medicine=medicine,
                quantity=quantity,
                total_price=total_price,
            )

            return render(request, "bill.html", {
                "bill": bill
            })

        return render(request, "sales.html", {
            "medicines": medicines_list,
            "error": "Insufficient medicine stock."
        })

    return render(request, "sales.html", {
        "medicines": medicines_list
    })


# =========================
# SALES HISTORY
# =========================

@login_required
def sales_history(request):

    sales_list = Sale.objects.all().order_by("-sale_date")

    return render(request, "sales_history.html", {
        "sales": sales_list
    })


# =========================
# BILLING HISTORY
# =========================

@login_required
def billing_history(request):

    bills = Bill.objects.all().order_by("-bill_date")

    return render(request, "billing_history.html", {
        "bills": bills
    })


# =========================
# H1 DRUG LIST
# =========================

@login_required
def h1_drugs(request):

    drugs = H1Drug.objects.all().order_by("-received_date")

    return render(request, "h1_drugs.html", {
        "drugs": drugs
    })


# =========================
# H1 DRUG SALE
# =========================

@login_required
def h1_drug_sale(request):

    drugs = H1Drug.objects.all().order_by("-received_date")

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        drug_id = request.POST.get("drug")
        quantity_text = request.POST.get("quantity")
        sale_price_text = request.POST.get("sale_price")

        # Quantity validation
        if not quantity_text:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "Please enter quantity."
            })

        # Sale price validation
        if not sale_price_text:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "Please enter sale price."
            })

        try:
            quantity = int(quantity_text)
            sale_price = float(sale_price_text)

        except ValueError:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "Please enter valid numbers."
            })

        try:
            drug = H1Drug.objects.get(id=drug_id)

        except H1Drug.DoesNotExist:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "H1 drug not found."
            })

        # Quantity check
        if quantity <= 0:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "Quantity must be greater than 0."
            })

        # Stock check
        if quantity > drug.quantity_received:
            return render(request, "h1_drug_sale.html", {
                "drugs": drugs,
                "error": "Insufficient H1 drug stock."
            })

        # Calculate total
        total_price = sale_price * quantity

        # Reduce stock
        drug.quantity_received -= quantity
        drug.save()

        # Create H1 sale bill
        bill = H1Sale.objects.create(
            customer_name=customer_name,
            drug=drug,
            quantity=quantity,
            sale_price=sale_price,
            total_price=total_price,
        )

        # Show bill
        return render(request, "h1_sale_bill.html", {
            "bill": bill
        })

    return render(request, "h1_drug_sale.html", {
        "drugs": drugs
    })


# =========================
# H1 SALE HISTORY
# =========================

@login_required
def h1_sale_history(request):

    sales_list = H1Sale.objects.all().order_by("-sale_date")

    return render(request, "h1_sale_history.html", {
        "sales": sales_list
    })


# =========================
# MEDICINE BOOKING
# =========================

@login_required
def book_medicine(request):

    medicines_list = Medicine.objects.filter(stock__gt=0)

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        address = request.POST.get("address")
        medicine_id = request.POST.get("medicine")
        quantity_text = request.POST.get("quantity")

        if not quantity_text:
            return render(request, "book_medicine.html", {
                "medicines": medicines_list,
                "error": "Please enter quantity."
            })

        try:
            quantity = int(quantity_text)

        except ValueError:
            return render(request, "book_medicine.html", {
                "medicines": medicines_list,
                "error": "Invalid quantity."
            })

        medicine = Medicine.objects.get(id=medicine_id)

        if quantity <= 0:
            return render(request, "book_medicine.html", {
                "medicines": medicines_list,
                "error": "Quantity must be greater than 0."
            })

        if quantity <= medicine.stock:

            booking = MedicineBooking.objects.create(
                customer_name=customer_name,
                mobile=mobile,
                email=email,
                address=address,
                medicine=medicine,
                quantity=quantity,
            )

            return render(request, "booking_success.html", {
                "customer_name": customer_name,
                "medicine": medicine,
                "quantity": quantity,
                "booking": booking,
            })

        return render(request, "book_medicine.html", {
            "medicines": medicines_list,
            "error": "Insufficient medicine stock."
        })

    return render(request, "book_medicine.html", {
        "medicines": medicines_list
    })


# =========================
# BOOKING HISTORY
# =========================

@login_required
def booking_history(request):

    bookings = MedicineBooking.objects.all().order_by("-booking_date")

    return render(request, "booking_history.html", {
        "bookings": bookings
    })