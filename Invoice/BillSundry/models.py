from django.db import models
import uuid

class InvoiceHeader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.IntegerField(auto_created=True)
    customer_name = models.CharField(max_length=255)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    gstin = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(InvoiceHeader, related_name='items', on_delete=models.CASCADE)

class InvoiceBillSundry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_sundry_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(InvoiceHeader, related_name='billsundrys', on_delete=models.CASCADE)
