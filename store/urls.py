from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("", views.home, name="home"),

    path("medicines/", views.medicines, name="medicines"),

    path("sales/", views.sales, name="sales"),

    path("sales-history/", views.sales_history, name="sales_history"),

    path("h1-drugs/", views.h1_drugs, name="h1_drugs"),

    path("h1-drug-sale/", views.h1_drug_sale, name="h1_drug_sale"),


    path("billing-history/", views.billing_history, name="billing_history"),

    path("book-medicine/", views.book_medicine, name="book_medicine"),
    
    path("booking-history/", views.booking_history, name="booking_history"),

]
