from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("medicines/", views.medicines, name="medicines"),

    path("sales/", views.sales, name="sales"),

    path("sales-history/", views.sales_history, name="sales_history"),

    path("h1-drugs/", views.h1_drugs, name="h1_drugs"),

    path("billing-history/", views.billing_history, name="billing_history"),

    path("book-medicine/", views.book_medicine, name="book_medicine"),
    
    path("booking-history/", views.booking_history, name="booking_history"),
]