
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    Medicine,
    Sale,
    Bill,
    H1Drug,
    H1Sale,
    MedicineBooking,
    GeneralProduct,
    GeneralSale,
    GeneralBill
)


# LOGIN
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


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect("login")


# DASHBOARD
@login_required
def home(request):
    total_medicines = Medicine.objects.count()
    total_sales = Sale.objects.count()
    total_bills = Bill.objects.count()

    low_stock = Medicine.objects.filter(stock__lte=10)

    return render(request, "home.html", {
        "total_medicines": total_medicines,
        "total_sales": total_sales,
        "total_bills": total_bills,
        "low_stock": low_stock,
        "low_stock_medicines": low_stock,
    })


# MEDICINES
@login_required
def medicines(request):
    search = request.GET.get("search", "")

    medicine_list = Medicine.objects.all().order_by("name")

    if search:
        medicine_list = medicine_list.filter(
            name__icontains=search
        )

    return render(request, "medicines.html", {
        "medicines": medicine_list,
        "search": search,
    })


# SALES
@login_required
def sales(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        medicine_id = request.POST.get("medicine")

        try:
            quantity = int(request.POST.get("quantity", 0))
        except (ValueError, TypeError):
            quantity = 0

        medicine = get_object_or_404(
            Medicine,
            id=medicine_id
        )

        if quantity <= 0 or quantity > medicine.stock:
            return render(request, "sales.html", {
                "medicines": Medicine.objects.all(),
                "error": "Invalid quantity or insufficient stock"
            })

        total_price = medicine.price * quantity

        sale = Sale.objects.create(
            customer_name=customer_name,
            medicine=medicine,
            quantity=quantity,
            total_price=total_price
        )

        bill = Bill.objects.create(
            customer_name=customer_name,
            medicine=medicine,
            quantity=quantity,
            total_price=total_price,
            created_by=request.user
        )

        medicine.stock -= quantity
        medicine.save()

        return render(request, "bill.html", {
            "bill": bill,
            "sale": sale
        })

    return render(request, "sales.html", {
        "medicines": Medicine.objects.all()
    })


# SALES HISTORY
@login_required
def sales_history(request):
    sales_list = Sale.objects.all().order_by("-sale_date")

    return render(request, "sales_history.html", {
        "sales": sales_list
    })


# BILLING HISTORY
@login_required
def billing_history(request):
    bills = Bill.objects.all().order_by("-bill_date")

    return render(request, "billing_history.html", {
        "bills": bills
    })


# H1 DRUGS
@login_required
def h1_drugs(request):
    if request.method == "POST":
        H1Drug.objects.create(
            drug_name=request.POST.get("drug_name"),
            batch_number=request.POST.get("batch_number"),
            quantity_received=int(
                request.POST.get("quantity_received", 0)
            ),
            supplier=request.POST.get("supplier"),
            received_date=request.POST.get("received_date"),
            expiry_date=request.POST.get("expiry_date"),
            remarks=request.POST.get("remarks", "")
        )

        return redirect("h1_drugs")

    drugs = H1Drug.objects.all().order_by("-received_date")

    return render(request, "h1_drugs.html", {
        "drugs": drugs
    })


# H1 DRUG SALE
@login_required
def h1_drug_sale(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        drug_id = request.POST.get("drug")

        try:
            quantity = int(request.POST.get("quantity", 0))
            sale_price = float(request.POST.get("sale_price", 0))
        except (ValueError, TypeError):
            quantity = 0
            sale_price = 0

        drug = get_object_or_404(
            H1Drug,
            id=drug_id
        )

        if quantity <= 0 or quantity > drug.quantity_received or sale_price <= 0:
            return render(request, "h1_drug_sale.html", {
                "drugs": H1Drug.objects.all(),
                "error": "Invalid quantity, sale price or insufficient stock"
            })

        total_price = sale_price * quantity

        bill = H1Sale.objects.create(
            customer_name=customer_name,
            drug=drug,
            quantity=quantity,
            sale_price=sale_price,
            total_price=total_price
        )

        drug.quantity_received -= quantity
        drug.save()

        return render(request, "h1_sale_bill.html", {
            "bill": bill
        })

    return render(request, "h1_drug_sale.html", {
        "drugs": H1Drug.objects.all()
    })


# H1 SALE HISTORY
@login_required
def h1_sale_history(request):
    sales_list = H1Sale.objects.all().order_by("-sale_date")

    return render(request, "h1_sale_history.html", {
        "sales": sales_list
    })


# BOOK MEDICINE
@login_required
def book_medicine(request):
    medicines_list = Medicine.objects.filter(stock__gt=0)

    medicine_id = (
        request.GET.get("medicine")
        or request.POST.get("medicine")
    )

    selected_medicine = None
    error = None

    if medicine_id:
        selected_medicine = get_object_or_404(
            medicines_list,
            id=medicine_id
        )

    if request.method == "POST":
        if not selected_medicine:
            error = "Please select a medicine."

        else:
            customer_name = request.POST.get("customer_name")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email", "")
            address = request.POST.get("address")

            try:
                quantity = int(request.POST.get("quantity", 0))
            except (ValueError, TypeError):
                quantity = 0

            if quantity <= 0:
                error = "Please enter a valid quantity."

            elif quantity > selected_medicine.stock:
                error = "Insufficient medicine stock."

            else:
                booking = MedicineBooking.objects.create(
                    customer_name=customer_name,
                    mobile=mobile,
                    email=email,
                    address=address,
                    medicine=selected_medicine,
                    quantity=quantity
                )

                return render(request, "booking_success.html", {
                    "booking": booking,
                    "medicine": selected_medicine,
                    "customer_name": customer_name,
                    "quantity": quantity
                })

    return render(request, "book_medicine.html", {
        "medicines": medicines_list,
        "selected_medicine": selected_medicine,
        "error": error
    })


# BOOKING HISTORY
@login_required
def booking_history(request):
    bookings = MedicineBooking.objects.all().order_by(
        "-booking_date"
    )

    return render(request, "booking_history.html", {
        "bookings": bookings
    })


# SEPARATE MEMBER BILLS
@login_required
def member_bills(request):
    bills = Bill.objects.filter(
        created_by=request.user
    ).order_by("-bill_date")

    return render(request, "member_bills.html", {
        "bills": bills
    })

# =====================================
# GENERAL STORE - PRODUCT LIST
# =====================================

@login_required
def general_store(request):
    search = request.GET.get("search", "")

    products = GeneralProduct.objects.all().order_by(
        "product_name"
    )

    if search:
        products = products.filter(
            product_name__icontains=search
        )

    return render(request, "general_store.html", {
        "products": products,
        "search": search
    })


# =====================================
# GENERAL STORE - ADD PRODUCT
# =====================================

@login_required
def add_general_product(request):
    if request.method == "POST":
        GeneralProduct.objects.create(
            product_name=request.POST.get("product_name"),
            category=request.POST.get("category"),
            brand=request.POST.get("brand", ""),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image=request.FILES.get("image")
        )

        return redirect("general_store")

    return render(request, "add_general_product.html")


# =====================================
# GENERAL STORE - DELETE PRODUCT
# =====================================

@login_required
def delete_general_product(request, product_id):
    product = get_object_or_404(
        GeneralProduct,
        id=product_id
    )

    if request.method == "POST":
        product.delete()
        return redirect("general_store")

    return render(request, "delete_general_product.html", {
        "product": product
    })


# =====================================
# GENERAL STORE - SALES AND BILLING
# =====================================

@login_required
def general_sales(request):
    products = GeneralProduct.objects.filter(
        stock__gt=0
    )

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        product_id = request.POST.get("product")

        try:
            quantity = int(request.POST.get("quantity", 0))
        except (ValueError, TypeError):
            quantity = 0

        product = get_object_or_404(
            GeneralProduct,
            id=product_id
        )

        if quantity <= 0 or quantity > product.stock:
            return render(request, "general_sales.html", {
                "products": products,
                "error": "Invalid quantity or insufficient stock"
            })

        total_price = product.price * quantity

        sale = GeneralSale.objects.create(
            customer_name=customer_name,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        bill = GeneralBill.objects.create(
            customer_name=customer_name,
            product=product,
            quantity=quantity,
            total_price=total_price,
            created_by=request.user
        )

        product.stock -= quantity
        product.save()

        return render(request, "general_bill.html", {
            "bill": bill,
            "sale": sale
        })

    return render(request, "general_sales.html", {
        "products": products
    })


# =====================================
# GENERAL STORE - SALES HISTORY
# =====================================

@login_required
def general_sales_history(request):
    sales_list = GeneralSale.objects.all().order_by(
        "-sale_date"
    )

    return render(request, "general_sales_history.html", {
        "sales": sales_list
    })


# =====================================
# GENERAL STORE - BILLING HISTORY
# =====================================

@login_required
def general_billing_history(request):
    bills = GeneralBill.objects.all().order_by(
        "-bill_date"
    )

    return render(request, "general_billing_history.html", {
        "bills": bills
    })


# =====================================
# GENERAL STORE - MEMBER BILLS
# =====================================

@login_required
def general_member_bills(request):
    bills = GeneralBill.objects.filter(
        created_by=request.user
    ).order_by("-bill_date")

    return render(request, "general_member_bills.html", {
        "bills": bills
    })
