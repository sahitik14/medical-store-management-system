from django.db import models


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    expiry_date = models.DateField()
    image = models.ImageField(upload_to="medicines/", blank=True, null=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class Bill(models.Model):
    bill_number = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    bill_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bill_number)


class H1Drug(models.Model):
    drug_name = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=100)
    quantity_received = models.IntegerField()
    supplier = models.CharField(max_length=150)
    received_date = models.DateField()
    expiry_date = models.DateField()
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.drug_name


class MedicineBooking(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Ready", "Ready"),
        ("Delivered", "Delivered"),
    ],
    default="Pending"
)
    

    def __str__(self):
        return self.customer_name