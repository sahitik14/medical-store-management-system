
from django.contrib import admin

from .models import (
    Medicine,
    Sale,
    Bill,
    H1Drug,
    H1Sale,
    MedicineBooking,
    GeneralProduct,
    GeneralSale,
    GeneralBill,
)


# =====================================
# MEDICAL STORE ADMIN CONFIGURATION
# =====================================
admin.site.site_header = "Medical Store Administration"
admin.site.site_title = "Medical Store Admin Portal"
admin.site.index_title = "Store Management & Control Panel"

original_admin_index = admin.site.index

def custom_admin_index(request, extra_context=None):
    from .models import Medicine, Sale, Bill, MedicineBooking, GeneralProduct, H1Drug
    extra = extra_context or {}
    try:
        extra["total_medicines"] = Medicine.objects.count()
        extra["low_stock_count"] = Medicine.objects.filter(stock__lte=10).count()
        extra["total_sales"] = Sale.objects.count()
        extra["total_bills"] = Bill.objects.count()
        extra["total_bookings"] = MedicineBooking.objects.count()
        extra["pending_bookings"] = MedicineBooking.objects.filter(status="Pending").count()
        extra["total_h1_drugs"] = H1Drug.objects.count()
        extra["total_general"] = GeneralProduct.objects.count()
    except Exception:
        pass
    return original_admin_index(request, extra_context=extra)

admin.site.index = custom_admin_index


# =====================================
# MEDICAL STORE ADMIN
# =====================================

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
        "created_by",
    )
    search_fields = ("customer_name",)


@admin.register(H1Drug)
class H1DrugAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "drug_name",
        "batch_number",
        "quantity_received",
        "supplier",
        "received_date",
        "expiry_date",
    )
    search_fields = ("drug_name", "batch_number")


@admin.register(H1Sale)
class H1SaleAdmin(admin.ModelAdmin):
    list_display = (
        "bill_number",
        "customer_name",
        "drug",
        "quantity",
        "sale_price",
        "total_price",
        "sale_date",
    )
    search_fields = ("customer_name",)


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


# =====================================
# GENERAL STORE ADMIN
# =====================================

@admin.register(GeneralProduct)
class GeneralProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "category",
        "brand",
        "price",
        "stock",
    )

    search_fields = (
        "product_name",
        "category",
        "brand",
    )

    list_filter = ("category",)


@admin.register(GeneralSale)
class GeneralSaleAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "product",
        "quantity",
        "total_price",
        "sale_date",
    )

    search_fields = (
        "customer_name",
        "product__product_name",
    )


@admin.register(GeneralBill)
class GeneralBillAdmin(admin.ModelAdmin):
    list_display = (
        "bill_number",
        "customer_name",
        "product",
        "quantity",
        "total_price",
        "bill_date",
        "created_by",
    )

    search_fields = (
        "customer_name",
        "product__product_name",
    )
