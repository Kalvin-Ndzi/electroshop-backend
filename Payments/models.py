from django.db import models
from Orders.models import Order
# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=200, choices=(
        ('MTN_MOMO','MTN Mobile Money'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('BANK_TRANSFER','Bank Transfer'),
    ))
    payment_status = models.CharField(max_length=200, choices= (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed','Failed'),
    ))