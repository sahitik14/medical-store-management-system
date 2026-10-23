from django.contrib import admin
from .models import Medicine, Sale, Bill, H1Drug, MedicineBooking


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "expiry_date",
    )
    search_fields = ("name", "category")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "medicine",
        "quantity",
        "sale_date",
    )


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "bill_number",
        "customer_name",
        "medicine",
        "quantity",
        "total_price",
        "bill_date",
    )


@admin.register(H1Drug)
class H1DrugAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(MedicineBooking)
class MedicineBookingAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "mobile",
        "email",
        "medicine",
        "quantity",
        "status",
        "booking_date",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "customer_name",
        "mobile",
        "email",
        "medicine__name",
    )