from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Medicine, Sale, Bill, H1Drug, MedicineBooking
from django.core.mail import send_mail

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


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    total_medicines = Medicine.objects.count()
    total_sales = Sale.objects.count()
    total_bills = Bill.objects.count()

    low_stock_medicines = Medicine.objects.filter(stock__lte=10)

    return render(request, "home.html", {
        "total_medicines": total_medicines,
        "total_sales": total_sales,
        "total_bills": total_bills,
        "low_stock": low_stock_medicines.count(),
        "low_stock_medicines": low_stock_medicines,
    })


@login_required
def medicines(request):
    medicine_list = Medicine.objects.all()

    return render(request, "medicines.html", {
        "medicines": medicine_list
    })


@login_required
def sales(request):
    medicines_list = Medicine.objects.all()

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        medicine_id = request.POST.get("medicine")
        quantity = int(request.POST.get("quantity"))

        medicine = Medicine.objects.get(id=medicine_id)

        if quantity <= medicine.stock:
            total_price = medicine.price * quantity

            sale = Sale.objects.create(
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
        "medicines": medicines_list
    })


@login_required
def sales_history(request):
    sales_list = Sale.objects.all().order_by("-sale_date")

    return render(request, "sales_history.html", {
        "sales": sales_list
    })

@login_required
def billing_history(request):
    bills = Bill.objects.all().order_by("-bill_date")

    return render(request, "billing_history.html", {
        "bills": bills
    })

@login_required
def h1_drugs(request):
    drugs = H1Drug.objects.all().order_by("-received_date")

    return render(request, "h1_drugs.html", {
        "drugs": drugs
    })

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

@login_required
def book_medicine(request):
    medicines_list = Medicine.objects.filter(stock__gt=0)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        address = request.POST.get("address")
        medicine_id = request.POST.get("medicine")
        quantity = int(request.POST.get("quantity"))

        medicine = Medicine.objects.get(id=medicine_id)

        if quantity <= medicine.stock:

            booking = MedicineBooking.objects.create(
                customer_name=customer_name,
                mobile=mobile,
                email=email,
                address=address,
                medicine=medicine,
                quantity=quantity,
            )

            send_mail(
                "Medicine Booking Confirmation",
                f"""
Hello {customer_name},

Your medicine booking has been successfully received.

Medicine: {medicine.name}
Quantity: {quantity}
Mobile: {mobile}
Address: {address}

Booking Status: {booking.status}

Thank you for using Medical Store Management System.
""",
                "noreply@medicalstore.com",
                [email],
                fail_silently=True,
            )

            return render(request, "booking_success.html", {
                "customer_name": customer_name,
                "medicine": medicine,
                "quantity": quantity,
            })

    return render(request, "book_medicine.html", {
        "medicines": medicines_list
    })

@login_required
def booking_history(request):
    bookings = MedicineBooking.objects.all().order_by("-booking_date")

    return render(request, "booking_history.html", {
        "bookings": bookings
    })