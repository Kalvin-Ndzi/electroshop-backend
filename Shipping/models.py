from django.db import models
from Orders.models import Order
# Create your models here.
class ShippingAgency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class ShippingCost(models.Model):
    agency = models.ForeignKey(ShippingAgency, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
