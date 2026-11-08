
from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # LOGIN / LOGOUT
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # MEDICAL STORE
    path("medicines/", views.medicines, name="medicines"),

    path("sales/", views.sales, name="sales"),
    path("sales-history/", views.sales_history, name="sales_history"),

    path("billing-history/", views.billing_history, name="billing_history"),

    path("book-medicine/", views.book_medicine, name="book_medicine"),
    path("booking-history/", views.booking_history, name="booking_history"),

    # H1 DRUGS
    path("h1-drugs/", views.h1_drugs, name="h1_drugs"),
    path("h1-drug-sale/", views.h1_drug_sale, name="h1_drug_sale"),
    path("h1-sale-history/", views.h1_sale_history, name="h1_sale_history"),

    # MEDICAL MEMBER BILLS
    path("member-bills/", views.member_bills, name="member_bills"),

    # GENERAL STORE
    path("general-store/", views.general_store, name="general_store"),

    path(
        "general-store/add/",
        views.add_general_product,
        name="add_general_product"
    ),

    path(
        "general-store/delete/<int:product_id>/",
        views.delete_general_product,
        name="delete_general_product"
    ),

    path(
        "general-store/sales/",
        views.general_sales,
        name="general_sales"
    ),

    path(
        "general-store/sales-history/",
        views.general_sales_history,
        name="general_sales_history"
    ),

    path(
        "general-store/billing-history/",
        views.general_billing_history,
        name="general_billing_history"
    ),

    path(
        "general-store/member-bills/",
        views.general_member_bills,
        name="general_member_bills"
    ),
]
